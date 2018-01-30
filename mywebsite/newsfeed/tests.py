from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse


class ChoiceModelTests(TestCase):
    def test_choice_repr(self):
        choice = Choice(choice_text="This is my choice")
        self.assertContains(choice, 'This is my choice')


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=12)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """
    See if the response when there are no question returns "no Polls are available" and
    that the context is an empty list
    """

    def test_no_question(self):
        response = self.client.get(reverse('newsfeed:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No news available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question("past question", days=-30)
        response = self.client.get(reverse('newsfeed:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past question>'])

    def test_future_question(self):
        create_question("future question", days=30)
        response = self.client.get(reverse('newsfeed:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_and_future_question(self):
        create_question("past question", days=-30)
        create_question("future_question", days=30)
        response = self.client.get(reverse('newsfeed:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past question>'])

    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('newsfeed:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        past_question = create_question(question_text='past question', days=-30)
        response = self.client.get(reverse('newsfeed:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        future_question = create_question(question_text="future question", days=30)
        response = self.client.get(reverse('newsfeed:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404, msg="Future questions should not be returned to the present")
