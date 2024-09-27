from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Tool(models.Model):
    ENERGY_CLASSES = [
        ('A+++', 'A+++'),
        ('A++', 'A++'),
        ('A+', 'A+'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    name = models.CharField(max_length=100, unique=True)
    co2_emission = models.FloatField(help_text="Emisja CO2 na jednostkę (ton)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
    #alternatives = models.ManyToManyField('self', blank=True, related_name='alternative_tools')
    image = models.CharField(max_length=100, blank=True)
    is_electric = models.BooleanField(default=False)
    energy_class = models.CharField(
        max_length=4,
        choices=ENERGY_CLASSES,
        null=True,
        blank=True,
        help_text="Klasa energetyczna (dotyczy tylko narzędzi elektrycznych)"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatyczne usunięcie klasy energetycznej, jeśli narzędzie nie jest elektryczne
        if not self.is_electric:
            self.energy_class = None
        super().save(*args, **kwargs)

class CO2Absorption(models.Model):
    source = models.CharField(max_length=100, unique=True)
    absorption_rate = models.FloatField(help_text="Pochłanianie CO2 (ton/rok)")

    def __str__(self):
        return self.source


