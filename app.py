from flask import Flask, render_template, request, url_for
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI rendering
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import io
import base64

app = Flask(__name__)

def generate_plots(N, mu, sigma2, S):

    # STEP 1
    # TODO 1: Generate a random dataset X of size N with values between 0 and 1
    # and a random dataset Y with normal additive error (mean mu, variance sigma^2).
    # Hint: Use numpy's random's functions to generate values for X and Y
    X = np.random.rand(N, 1)  # Generate random values for X between 0 and 1
    Y = mu + np.sqrt(sigma2) * np.random.randn(N, 1)  # Generate random Y values with normal error


    # TODO 2: Fit a linear regression model to X and Y
    # Hint: Use Scikit Learn
    model = LinearRegression()
    model.fit(X, Y)
    slope = model.coef_[0][0]
    intercept = model.intercept_[0]

    # TODO 3: Generate a scatter plot of (X, Y) with the fitted regression line
    plot1_path = "static/plot1.png"
    plt.figure(figsize=(8, 6))
    plt.scatter(X, Y, color='black', alpha=0.5, label='Data Points')
    plt.plot(X, model.predict(X), color='red', label=f'Regression Line: y = {slope:.2f}x + {intercept:.2f}')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Scatter Plot with Regression Line (y = {slope:.2f}x + {intercept:.2f})")
    plt.legend()
    plt.savefig(plot1_path)
    plt.close()
    # Replace the above TODO 3 block with code to generate and save the plot

    
    # Step 2: Run S simulations and create histograms of slopes and intercepts

    # TODO 1: Initialize empty lists for slopes and intercepts
    # Hint: You will store the slope and intercept of each simulation's linear regression here.
    slopes = []  # Replace with code to initialize empty list
    intercepts = []  # Replace with code to initialize empty list

    # TODO 2: Run a loop S times to generate datasets and calculate slopes and intercepts
    # Hint: For each iteration, create random X and Y values using the provided parameters
    for _ in range(S):
        X_sim = np.random.rand(N, 1)
        Y_sim = mu + np.sqrt(sigma2) * np.random.randn(N, 1)

        sim_model = LinearRegression()
        sim_model.fit(X_sim, Y_sim)

        slopes.append(sim_model.coef_[0][0])
        intercepts.append(sim_model.intercept_[0])


    # Plot histograms of slopes and intercepts
    plt.figure(figsize=(10, 5))
    plt.hist(slopes, bins=20, alpha=0.5, color="blue", label="Slopes")
    plt.hist(intercepts, bins=20, alpha=0.5, color="orange", label="Intercepts")
    plt.axvline(slope, color="blue", linestyle="--", linewidth=1, label=f"Slope: {slope:.2f}")
    plt.axvline(intercept, color="orange", linestyle="--", linewidth=1, label=f"Intercept: {intercept:.2f}")
    plt.title("Histogram of Slopes and Intercepts")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plot2_path = "static/plot2.png"
    plt.savefig(plot2_path)
    plt.close()

    # Below code is already provided
    # Calculate proportions of more extreme slopes and intercepts
    # For slopes, we will count how many are greater than the initial slope; for intercepts, count how many are less.
    slope_more_extreme = sum(s > slope for s in slopes) / S  # Already provided
    intercept_more_extreme = sum(i < intercept for i in intercepts) / S  # Already provided

    return plot1_path, plot2_path, slope_more_extreme, intercept_more_extreme

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        N = int(request.form["N"])
        mu = float(request.form["mu"])
        sigma2 = float(request.form["sigma2"])
        S = int(request.form["S"])

        # Generate plots and results
        plot1, plot2, slope_extreme, intercept_extreme = generate_plots(N, mu, sigma2, S)

        return render_template("index.html", plot1=plot1, plot2=plot2,
                               slope_extreme=slope_extreme, intercept_extreme=intercept_extreme)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)