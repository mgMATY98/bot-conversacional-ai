from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.ip_blocks import IPBlock

BLOCK_HOURS = 24
MAX_ATTEMPTS = 5
now = datetime.now(timezone.utc)


def is_ip_blocked(db: Session, ip: str) -> bool:
    """
    Devuelve True si la IP está bloqueada.
    """

    block = db.query(IPBlock).filter(IPBlock.ip == ip).first()

    if not block:
        return False

    if block.blocked_until is None:
        return False

    return block.blocked_until > now


def register_failed_attempt(db: Session, ip: str):

    block = db.query(IPBlock).filter(IPBlock.ip == ip).first()

    if not block:

        block = IPBlock(
            ip=ip,
            failed_attempts=1,
            last_attempt=now,
        )

        db.add(block)

    else:

        block.failed_attempts += 1
        block.last_attempt = now

        if block.failed_attempts >= MAX_ATTEMPTS:

            block.blocked_until = now + timedelta(hours=BLOCK_HOURS)

    db.commit()


def reset_failed_attempts(db: Session, ip: str):

    block = db.query(IPBlock).filter(IPBlock.ip == ip).first()

    if not block:
        return

    block.failed_attempts = 0
    block.blocked_until = None

    db.commit()
