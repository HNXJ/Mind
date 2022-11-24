from dash import Dash, html, dcc
import dash


app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    use_pages=True
)

LAB_WEBSITE = "http://bastoslabvu.com"

app.layout = html.Div([
	html.H1('Electrophysiology signal/data analysis GUI'),
    html.Div(
        [
            html.A(
                "Return to the lab website",
                href=LAB_WEBSITE,
                target="_blank",
            )
        ],
        className="header__button",
    ),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)