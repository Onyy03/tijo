from datetime import datetime

from app.accounts.service import AccountService
from app.clock import Clock
from app.codes.generator import CodeGenerator
from app.codes.models import BlikCode
from app.codes.repository import BlikCodeRepository

MAX_GENERATION_ATTEMPTS = 10


class BlikCodeService:
    def __init__(
        self,
        accounts: AccountService,
        codes: BlikCodeRepository,
        generator: CodeGenerator,
        clock: Clock,
    ) -> None:
        self._accounts = accounts
        self._codes = codes
        self._generator = generator
        self._clock = clock

    def generate_code(self, account_id: int) -> BlikCode:
        account = self._accounts.get_account(account_id)
        now = self._clock.now()
        for previous_code in self._codes.find_active_by_account(account.id):
            previous_code.cancel()
        blik_code = BlikCode.issue(account.id, self._draw_free_code(now), now)
        self._codes.add(blik_code)
        return blik_code

    def _draw_free_code(self, now: datetime) -> str:
        for _ in range(MAX_GENERATION_ATTEMPTS):
            code = self._generator.generate()
            if not self._codes.is_code_in_use(code, now):
                return code
        raise RuntimeError("Could not draw a free BLIK code")
