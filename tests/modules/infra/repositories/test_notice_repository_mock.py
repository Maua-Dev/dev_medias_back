import pytest
import uuid

from src.shared.domain.entities.notice import Notice
from src.shared.domain.enums.severity_enum import SEVERITY
from src.shared.infra.repositories.notice_repository_mock import NoticeRepositoryMock
from src.shared.helpers.errors.controller_errors import MissingParameters


class TestNoticeRepositoryMock:
    def test_get_all_notices_returns_initial_notices(self):
        repo = NoticeRepositoryMock()

        notices = repo.get_all_notices()

        assert isinstance(notices, list)
        assert len(notices) == 3
        assert all(isinstance(item, Notice) for item in notices)

    def test_get_notice_returns_existing_notice(self):
        repo = NoticeRepositoryMock()
        existing_notice = repo.get_all_notices()[0]

        fetched = repo.get_notice(existing_notice.id)

        assert fetched == existing_notice

    def test_get_notice_returns_none_for_missing_notice(self):
        repo = NoticeRepositoryMock()

        fetched = repo.get_notice("missing-id")

        assert fetched is None

    def test_create_notice_appends_and_returns_new_notice(self):
        repo = NoticeRepositoryMock()
        new_notice = Notice(
            id=str(uuid.uuid4()),
            title="Novo Aviso",
            description="Descrição do novo aviso",
            severity=SEVERITY.LOW,
        )

        created = repo.create_notice(new_notice)

        assert created is new_notice
        assert repo.get_notice(new_notice.id) == new_notice
        assert new_notice in repo.get_all_notices()

    def test_update_notice_changes_existing_notice_fields(self):
        repo = NoticeRepositoryMock()
        notice = repo.get_all_notices()[0]

        updated = repo.update_notice(
            id=notice.id,
            title="Aviso Atualizado",
            description="Descrição atualizada",
            severity=SEVERITY.MEDIUM,
        )

        assert updated.id == notice.id
        assert updated.title == "Aviso Atualizado"
        assert updated.description == "Descrição atualizada"
        assert updated.severity == SEVERITY.MEDIUM
        assert repo.get_notice(notice.id).title == "Aviso Atualizado"

    def test_update_notice_missing_id_raises_missing_parameters(self):
        repo = NoticeRepositoryMock()

        with pytest.raises(MissingParameters, match="id"):
            repo.update_notice(
                id=None,
                title="Title",
                description="Description",
                severity=SEVERITY.HIGH,
            )

    def test_update_notice_not_found_raises_value_error(self):
        repo = NoticeRepositoryMock()

        with pytest.raises(ValueError, match="Notice not found"):
            repo.update_notice(
                id="missing-id",
                title="Title",
                description="Description",
                severity=SEVERITY.HIGH,
            )

    def test_delete_notice_removes_existing_notice(self):
        repo = NoticeRepositoryMock()
        notice = repo.get_all_notices()[0]

        deleted = repo.delete_notice(notice.id)

        assert deleted == notice
        assert repo.get_notice(notice.id) is None
        assert notice not in repo.get_all_notices()

    def test_delete_notice_not_found_raises_value_error(self):
        repo = NoticeRepositoryMock()

        with pytest.raises(ValueError):
            repo.delete_notice("missing-id")
