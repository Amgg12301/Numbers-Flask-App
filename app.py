import requests, random as rand
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# Results for selected number and fact categories if requested for
@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        number = request.form['number']
        fact_types = request.form.getlist('fact')
        response = []
        urls = []
        result = ""

        for fact in fact_types:
            result = requests.get("http://numbersapi.com/" + str(number) + "/" + fact.lower()).text
            result = checkUninterestingNumbers(number, result, fact.lower())
            response.append(result)

        for result in response:
            urls.append(googleSearch(result))

        return render_template("results.html", response=response, number=number, urls=urls,
                               response_and_urls=zip(response, urls))


# Random numbers, fact categories, and results if requested for
@app.route("/random", methods=['GET', 'POST'])
def random():
    if request.method == 'POST':
        amount = int(request.form['numbers'])
        maximum = int(request.form['maximum'])
        trivia = int(request.form['randomtrivia'])
        math = int(request.form['randommath'])
        date = int(request.form['randomdate'])
        year = int(request.form['randomyear'])
        response = []
        urls = []
        info = ""
        number = 0
        total = trivia + math + date + year

        if amount != total:
            if amount > total:
                trivia += (amount - total)
            else:
                math -= (total - amount)
        if maximum == 0:
            maximum = 500

        for i in range(0, trivia):
            number = rand.randrange(maximum)
            print(number)
            info = requests.get("http://numbersapi.com/" + str(number) + "/trivia").text
            info = checkUninterestingNumbers(number, info, "trivia")
            response.append(info)
        for i in range(0, math):
            number = rand.randrange(maximum)
            print(number)
            info = requests.get("http://numbersapi.com/" + str(number) + "/math").text
            print(info)
            info = checkUninterestingNumbers(number, info, "math")
            print(info)
            response.append(info)
        for i in range(0, date):
            number = rand.randrange(maximum)
            print(number)
            info = requests.get("http://numbersapi.com/" + str(number) + "/date").text
            info = checkUninterestingNumbers(number, info, "date")
            response.append(info)
        for i in range(0, year):
            number = rand.randrange(maximum)
            print(number)
            info = requests.get("http://numbersapi.com/" + str(number) + "/year").text
            info = checkUninterestingNumbers(number, info, "year")
            response.append(info)
        for result in response:
            urls.append(googleSearch(result))

        return render_template("random.html", response=response, number=number, urls=urls,
                               response_and_urls=zip(response, urls))


# Method for uninteresting numbers / numbers with no results
def checkUninterestingNumbers(number, result, type):
    end_result = ""
    conditions = {"is a boring number", "undefined", "missing a fact", "uninteresting", "unremarkable",
                  "nothing remarkable",
                  "nothing interesting", "year that the Earth probably went around the Sun"}

    if "Bad Gateway" in result:
        end_result = "Looks like there is an issue with the Numbers API response for a " + str(
            type) + " fact for the number " + \
                     str(number) + " at the moment, sorry :("
        return end_result
    elif any(x in result for x in conditions):
        if str(type) == "date":
            end_result = requests.get("http://numbersapi.com/" + str(number) + "?notfound=floor").text
        else:
            end_result = requests.get("http://numbersapi.com/" + str(number) + "/" + str(type) + "?notfound=floor").text
        fact = "Since we couldn't find anything for " + str(type) + " for a " + str(
            number) + " fact, here's a fact for another number: " + end_result
        return fact
    else:
        return result


# Method for getting google search result url
def googleSearch(result):
    new_result = ""

    if "Since we couldn't find anything for " in result:
        new_result = result[86:]
    else:
        new_result = result
    words = new_result.split()
    url = "http://google.com/search?q="

    for word in words:
        if words.index(word) == len(words) - 1:
            url += word
        else:
            url += word + "+"

    return url


if __name__ == "__main__":
    app.run(debug=True, port=0)
