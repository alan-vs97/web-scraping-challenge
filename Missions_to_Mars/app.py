from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

@app.route("/")
def home():

    # Connect to mongo
    conn_str = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn_str)
    db = client.mars_db

    data = db.mars_info.find()

    title_news = data[0]["news_title"]
    p_news = data[0]["news_p"]
    featured_image_url = data[0]["featured_image"]
    weather_text = data[0]["weather"]
    hemisphere_image_urls = data[0]["hemispheres"]
    table_html = data[0]["table"]

    return render_template("index.html", title_news=title_news, p_news=p_news, featured_image_url=featured_image_url, weather_text=weather_text, table_html=table_html, hemisphere_image_urls=hemisphere_image_urls)


@app.route("/scrape")
def new_data():

    title_news, p_news, featured_image_url, weather_text, hemisphere_image_urls, table_html = scrape_mars.scrape()

    scrape_dict = {
        "news_title": title_news,
        "news_p": p_news,
        "featured_image": featured_image_url,
        "weather": weather_text,
        "hemispheres": hemisphere_image_urls,
        "table": table_html
    }

    # Connect to mongo
    conn_str = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn_str)
    db = client.mars_db

    # Clear the old data

    db.mars_info.delete_many({})

    db.mars_info.insert_one(
        scrape_dict
    )

    # After getting new data, return to the index, so that you can instantly see the results
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
