import json
from importlib import resources

from PIL import Image

from hockey.transform.shots import shots_from_pbp, standings_table
from hockey.viz import charts, style


def _sample(name):
    return json.loads(resources.files("hockey.sample_data").joinpath(name).read_text())


def test_scatter_is_exactly_1080_square(tmp_path):
    df = standings_table(_sample("standings_sample.json"))
    path = style.save(charts.team_scatter(df, sample=True), "t", out_dir=tmp_path)
    assert Image.open(path).size == (1080, 1080)


def test_shot_map_portrait_size(tmp_path):
    shots = shots_from_pbp(_sample("pbp_sample.json"))
    post = charts.shot_map(shots, "HOM", "AWY", "Nov 1", sample=True, size="portrait")
    assert Image.open(style.save(post, "t", out_dir=tmp_path)).size == (1080, 1350)


def test_both_themes_render_with_their_background(tmp_path):
    df = standings_table(_sample("standings_sample.json"))
    for name, theme in style.THEMES.items():
        path = style.save(charts.team_scatter(df, theme=name), name, out_dir=tmp_path)
        corner = Image.open(path).convert("RGB").getpixel((2, 2))
        assert "#{:02X}{:02X}{:02X}".format(*corner) == theme["BG"].upper()
