from app import app

def test_header_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout=4)
    header_text = dash_duo.find_element("h1").text
    assert "Soul Foods Pink Morsel Sales Performance" in header_text

def test_visualization_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-line-chart", timeout=4)
    chart = dash_duo.find_element("#sales-line-chart")
    assert chart is not None

def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=4)
    picker = dash_duo.find_element("#region-filter")
    assert picker is not None
