def get_graph_data():

    return {

        "nodes": [

            {
                "id": "nvda",
                "label": "NVIDIA",
                "sector": "Semiconductors"
            },

            {
                "id": "tsmc",
                "label": "TSMC",
                "sector": "Semiconductors"
            },

            {
                "id": "aws",
                "label": "AWS",
                "sector": "Cloud"
            }

        ],

        "edges": [

            {
                "source": "nvda",
                "target": "tsmc",
                "relation": "chip demand"
            },

            {
                "source": "nvda",
                "target": "aws",
                "relation": "AI infrastructure"
            }

        ]
    }