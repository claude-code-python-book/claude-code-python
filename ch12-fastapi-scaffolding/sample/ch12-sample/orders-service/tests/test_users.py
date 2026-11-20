import pytest

from orders.users import InMemoryUserRepository, User, authenticate

DUMMY = "dummy-hash"


class FakeHasher:
    """Stands in for pwdlib: the 'hash' of a password is 'h:' + password."""

    def __init__(self) -> None:
        self.checked: list[str] = []

    def verify(self, password: str, hashed: str) -> bool:
        self.checked.append(hashed)
        return hashed == f"h:{password}"


@pytest.fixture
def users() -> InMemoryUserRepository:
    repo = InMemoryUserRepository()
    repo.add(User("alice", "C-1001", "h:right"))
    repo.add(User("bob", "C-2002", "h:right", disabled=True))
    return repo


def test_right_password_returns_the_user(users: InMemoryUserRepository) -> None:
    user = authenticate(
        users, "alice", "right", verify=FakeHasher().verify, dummy_hash=DUMMY
    )
    assert user is not None
    assert user.customer_id == "C-1001"


@pytest.mark.parametrize(("name", "password"), [("alice", "wrong"), ("bob", "right")])
def test_wrong_password_or_disabled_account_fails(
    users: InMemoryUserRepository, name: str, password: str
) -> None:
    assert (
        authenticate(
            users, name, password, verify=FakeHasher().verify, dummy_hash=DUMMY
        )
        is None
    )


def test_unknown_user_still_runs_a_password_check(
    users: InMemoryUserRepository,
) -> None:
    hasher = FakeHasher()
    assert (
        authenticate(users, "mallory", "x", verify=hasher.verify, dummy_hash=DUMMY)
        is None
    )
    assert hasher.checked == [DUMMY]
