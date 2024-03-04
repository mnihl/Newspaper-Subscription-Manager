from src.app import create_app

if __name__ == '__main__':
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    print(response)
    create_app().run(debug=False, port=7890)
