from django.db import models

class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    series = models.CharField(max_length=10)
    number = models.CharField(max_length=20)
    issue_date = models.DateField()
    issued_by = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.series} {self.number}"


class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='guests')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.full_name


class RoomCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AmenityItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CategoryAmenity(models.Model):
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    amenity_item = models.ForeignKey(AmenityItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('room_category', 'amenity_item')

    def __str__(self):
        return f"{self.room_category} — {self.amenity_item}"


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    floor = models.IntegerField()
    num_rooms = models.IntegerField()
    sleeping_capacity = models.IntegerField()
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return f"Room {self.room_id} (Floor {self.floor}, {self.sleeping_capacity} beds)"


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking {self.booking_id} — {self.guest} ({self.check_in} to {self.check_out})"


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ServiceRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='records')
    quantity = models.IntegerField(default=1)
    service_date = models.DateField()

    def __str__(self):
        return f"{self.service} x{self.quantity} for booking {self.booking.booking_id}"