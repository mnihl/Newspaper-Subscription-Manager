def test_update_editor(agency):
    agency.editors = []
    new_editor = Editor(editor_id=1,
                        name="John Doe",
                        address="1234 Main St")
    agency.new_editor(new_editor)
    assert agency.get_editor(1).name == "John Doe"
    assert agency.get_editor(1).address == "1234 Main St"

    data = {
        'name': 'Jane Doe',
        'address': '5678 Main St'
    }

    updated_editor = agency.update_editor(1, data)
    print(updated_editor)
    assert updated_editor.name == "Jane Doe"
    assert updated_editor.address == "5678 Main St"