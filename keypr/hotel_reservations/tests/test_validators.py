from django.test import TestCase
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock
import datetime
from hotel_reservations.validators import (is_valid_date_range, is_available,
                                           is_positive, is_not_negative,
                                           is_email_address, is_future_date)


class TestValidators(TestCase):
    def test_is_positive(self):
        valid_numbers = [1, 1.2, 1234567890]
        try:
            for number in valid_numbers:
                is_positive(number)
        except ValidationError:
            self.fail("ValidationError raised unexpectedly")
        invalid_numbers = [0, -0.5, -9876543210]
        for number in invalid_numbers:
            with self.assertRaises(ValidationError):
                is_positive(number)

    def test_not_negative(self):
        valid_numbers = [0, 1.2, 1234567890]
        try:
            for number in valid_numbers:
                is_not_negative(number)
        except ValidationError:
            self.fail("ValidationError raised unexpectedly")
        invalid_numbers = [-1, -0.5, -9876543210]
        for number in invalid_numbers:
            with self.assertRaises(ValidationError):
                is_not_negative(number)

    def test_is_email_address(self):
        valid_emails = [
            "real@example.com",
            "fake@fake.fake",
            "some.long-convoluted--email{}with+crazy()characters@sub-domain.some_domain.co.uk"
        ]
        try:
            for email in valid_emails:
                is_email_address(email)
        except ValidationError:
            self.fail("ValidationError raised unexpectedly")
        invalid_emails = [
            "not even trying",
            "too@many@at.symbols",
            "disallowed.character@in+domain.biz"
        ]
        for email in invalid_emails:
            with self.assertRaises(ValidationError):
                is_email_address(email)

    def test_is_valid_date_range(self):
        valid_date_pairs = [
            (datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date(),
             datetime.datetime.strptime('2018-01-02', '%Y-%m-%d').date()),
            (datetime.datetime.strptime('0001-01-01', '%Y-%m-%d').date(),
             datetime.datetime.strptime('2018-01-02', '%Y-%m-%d').date()),
            (datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date(),
             datetime.datetime.strptime('9999-01-02', '%Y-%m-%d').date())
        ]
        try:
            for date_pair in valid_date_pairs:
                is_valid_date_range(*date_pair)
        except ValidationError:
            self.fail("ValidationError raised unexpectedly")
        invalid_date_pairs = [
            (datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date(),
             datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date()),
            (datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date(),
             datetime.datetime.strptime('0001-01-02', '%Y-%m-%d').date()),
            (datetime.datetime.strptime('9999-01-01', '%Y-%m-%d').date(),
             datetime.datetime.strptime('2018-01-02', '%Y-%m-%d').date())
        ]
        for date_pair in invalid_date_pairs:
            with self.assertRaises(ValidationError):
                is_valid_date_range(*date_pair)

    @patch("hotel_reservations.validators.datetime.date")
    def test_is_future_date(self, mock_date):
        mock_date.today.return_value = datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date()
        valid_dates = [
            datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date(),
            datetime.datetime.strptime('2018-12-31', '%Y-%m-%d').date(),
            datetime.datetime.strptime('9999-01-01', '%Y-%m-%d').date()
        ]
        try:
            for date in valid_dates:
                is_future_date(date)
        except ValidationError:
            self.fail("ValidationError raised unexpectedly")
        invalid_dates = [
            datetime.datetime.strptime('2017-01-01', '%Y-%m-%d').date(),
            datetime.datetime.strptime('2017-12-31', '%Y-%m-%d').date(),
            datetime.datetime.strptime('0001-01-01', '%Y-%m-%d').date()
        ]
        for date in invalid_dates:
            with self.assertRaises(ValidationError):
                is_future_date(date)
    
    @patch("hotel_reservations.models.HotelConfiguration.get_solo")
    @patch("hotel_reservations.models.Reservation.objects.filter")
    def test_is_available(self, mock_filter, mock_solo):
        reservation_count = 0
        filter = MagicMock()
        filter.count = lambda: reservation_count
        solo = MagicMock()
        mock_solo.return_value = solo
        mock_filter.return_value = filter
        date_pair = (datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date(),
                     datetime.datetime.strptime('2018-01-02', '%Y-%m-%d').date())
        try:
            reservation_count = 0
            solo.room_count = 100
            solo.overbooking_level = 0
            is_available(*date_pair)

            reservation_count = 109
            solo.room_count = 100
            solo.overbooking_level = 0.1
            is_available(*date_pair)

            reservation_count = 199
            solo.room_count = 100
            solo.overbooking_level = 1
        except ValidationError:
            self.fail("ValidationError raised unexpectedly")

        reservation_count = 110
        solo.room_count = 100
        solo.overbooking_level = 0
        with self.assertRaises(ValidationError):
            is_available(*date_pair)
        
        reservation_count = 110
        solo.room_count = 100
        solo.overbooking_level = 0.1
        with self.assertRaises(ValidationError):
            is_available(*date_pair)
        
        reservation_count = 200
        solo.room_count = 100
        solo.overbooking_level = 1
        with self.assertRaises(ValidationError):
            is_available(*date_pair)
