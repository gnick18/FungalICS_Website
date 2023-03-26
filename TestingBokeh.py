from dna_features_viewer import GraphicFeature, GraphicRecord
import bokeh
from bokeh.plotting import figure, output_file, save, show
from bokeh.embed import file_html
from bokeh.resources import CDN

features=[
    GraphicFeature(start=0, end=20, strand=+1, color="#ffd700",
                   label="Small feature", html="TESTY TEST", label_link_color="auto"),
    GraphicFeature(start=20, end=500, strand=+1, color="#ffcccc",
                   label="Gene 1 with a very long name",html="TESTY TEST",label_link_color="auto"),
    GraphicFeature(start=400, end=700, strand=-1, color="#cffccc",
                   label="Gene 2",html="TESTY TEST",label_link_color="auto"),
    GraphicFeature(start=600, end=900, strand=+1, color="#ccccff",
                   label="Gene 3",html="TESTY TEST",label_link_color="auto")
]
record = GraphicRecord(sequence_length=1000, features=features)
plot = record.plot_with_bokeh(figure_width=5, figure_height="auto")

html = file_html(plot, CDN, title="BGC NAME")

outPath = "test.html"
with open(outPath, "w") as out:
    out.write(html)


