def test_dispatch():
    from .dispatcher import dispatch_input
    class FakeRequest:
        def get_json(self): return { "question": "2x + 5 = 13" }
    print(dispatch_input(FakeRequest()))
