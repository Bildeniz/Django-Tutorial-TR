import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Questions

# Create your tests here.

def create_question(question_text, days):
    """
    Verilen `question_text` ile bir Questions nesnesi oluşturun ve
    şu ana kadar verilen `days` sayısı (yayınlanan Questions için negatif
    geçmişte, henüz yayınlanmamış Questions için pozitif).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Questions.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Eğer Questions nesnesi yoksa uygun bir mesaj görüntülenir
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Soru bulunamadı!")
        self.assertQuerySetEqual(response.context['latest_questions_list'], [])

    def test_past_questions(self):
        """
        Geçmişteki Questions nesneleri `pub_date` ile `index` üzerinde 
        görüntülenmesi
        """
        question = create_question(question_text="Geçmiş Questions", days=-30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerySetEqual(
            response.context['latest_questions_list'],
            [question],
        )

    def test_future_questions(self):
        """
        Gelecekteki Questions nesneleri `pub_date` ile `index` üzerinde 
        görüntülenmemesi
        """
        create_question(question_text="Gelecek Questions", days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerySetEqual(
            response.context['latest_questions_list'],
            [],
        )

    def test_future_questions_and_past_questions(self):
        """
        Hem geçmiş hem de gelecek `Questions` mevcut olsa bile, sadece geçmiş `Questions` 
        nesneleri görüntülenir.
        """
        question = create_question(question_text="Geçmiş questions", days=-30)
        create_question(question_text="Gelecek questions", days=30)

        response = self.client.get(reverse('polls:index'))

        self.assertQuerySetEqual(
            response.context['latest_questions_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        `Index` sayfası için birden fazla `Questions` nesnesi görüntülenir.
        """        

        question = create_question(question_text="Geçmiş question 1", days=-30)
        question2 = create_question(question_text="Geçmiş question 2", days=-15)

        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_questions_list'],
            [question2, question]
        )

class QuestionsDetailViewTests(TestCase):
    def test_future_question(self):
        """
        `pub_date`'i gelecekte olan bir `Question` nesnesinin details görünümü
        404 bulunamadı döndürür.
        """

        future_question = create_question(question_text="Gelecek questions.", days=5)
        url = reverse('polls:details', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        `Pub_date`'i geçmişte olan bir `Question` nesnesinin ayrıntı görünümü ve
        metnini görüntüler.
        """
        
        past_question = create_question(question_text="Geçmiş questions", days=-5)
        url = reverse('polls:details', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionsModelTests(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently() False döndürmesi gerekiyor Questions sınıfı için 
        eğer pub_date gelecekte ise.
        """

        future_question = create_question(question_text="Gelecek questions", days=30)

        self.assertIs(future_question.was_published_recently(), 
                      False, 
                      msg="Gelecekte yazılan bir soru son günlerde yayınlanmış(Future pub_date error)")

    def test_was_published_recently_with_old_questions(self):
        """
        was_published_recently() False döndürmesi gerekiyor Questions sınıfı içi
        eğer pub_date 1 günden eski ise.
        """

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Questions(pub_date=time)

        self.assertIs(old_question.was_published_recently(), 
                      False, 
                      "False döndürmesi gerekiyordu çünkü 1 günden eski tarihte yayınlanmış")
        
    def test_was_published_recently_with_recent_questions(self):
        """
        was_published_recently() True döndürmesi gerekiyor Questions sınıfı içi
        eğer pub_date 1 günden yeni ise.
        """

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        old_question = Questions(pub_date=time)

        self.assertIs(old_question.was_published_recently(),
                      True,
                      msg="True Döndürmesi gerekiyordu çünkü 1 günden yeni tarihte yayınlanmış")