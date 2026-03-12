from app import app


def run_smoke_test():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    print("Smoke test passed: index route returned 200")


if __name__ == "__main__":
    run_smoke_test()
