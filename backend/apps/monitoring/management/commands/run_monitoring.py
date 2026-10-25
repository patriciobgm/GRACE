from django.core.management.base import BaseCommand
from apps.monitoring.services import run_monitoring
class Command(BaseCommand):
    help = "Evaluate deterministic GRACE monitoring rules"
    def handle(self, *args, **options): self.stdout.write(self.style.SUCCESS(f"Created {run_monitoring()} new alert(s)."))

