from learning_app import user_service


def test_get_user_label_formats_user(mocker, sample_user: dict[str, object]) -> None:
    fetch_user = mocker.patch(
        "learning_app.user_service.fetch_user",
        return_value=sample_user,
    )

    label = user_service.get_user_label("https://example.test", 7)

    assert label == "Lin (#7)"
    fetch_user.assert_called_once_with("https://example.test", 7)
