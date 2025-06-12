# Since all the formulas looked the same I removed redundant operations to minimize code length
def sum_helper(x_list, power_x, y_list, power_y):
    ans = 0
    i = 0
    size = max(len(x_list), len(y_list))
    while i < size:
        temp = 1
        if power_x > 0:
            temp *= x_list[i] ** power_x
        if power_y > 0:
            temp *= y_list[i] ** power_y
        ans += temp
        i += 1
    return ans


# formula obtained from https://www.azdhs.gov/documents/preparedness/state-laboratory/lab-licensure-certification/technical-resources/calibration-training/12-quadratic-least-squares-regression-calib.pdf
# Used the above formula to perform quadratic regression with the points as parameters to the function
def quadratic_regression(x_list, y_list):
    n = len(x_list)
    sxx = sum_helper(x_list, 2, [], 0) - (sum_helper(x_list, 1, [], 0) ** 2) / n
    sxy = sum_helper(x_list, 1, y_list, 1) - (sum_helper(x_list, 1, [], 0) * sum_helper([], 0, y_list, 1)) / n
    sxx2 = sum_helper(x_list, 3, [], 0) - (sum_helper(x_list, 1, [], 0) * sum_helper(x_list, 2, [], 0)) / n
    sx2y = sum_helper(x_list, 2, y_list, 1) - (sum_helper(x_list, 2, [], 0) * sum_helper([], 0, y_list, 1)) / n
    sx2x2 = sum_helper(x_list, 4, [], 0) - (sum_helper(x_list, 2, [], 0) ** 2) / n
    sx = sum_helper(x_list, 1, [], 0)
    sy = sum_helper([], 0, y_list, 1)
    sx2 = sum_helper(x_list, 2, [], 0)
    a = ((sx2y * sxx) - (sxy * sxx2)) / ((sxx * sx2x2) - (sxx2 ** 2))
    b = ((sxy * sx2x2) - (sx2y * sxx2)) / ((sxx * sx2x2) - (sxx2 ** 2))
    c = (sy / n) - (b * (sx / n)) - (a * sx2 / n)
    # returned coeff to be later parsed for output by the parser function
    return (a, b, c)


# formula obtained from https://www.ncl.ac.uk/webtemplate/ask-assets/external/maths-resources/statistics/regression-and-correlation/simple-linear-regression.html#:~:text=The%20simple%20linear%20regression%20line%2C%20%5Ey%3Da%2Bb,every%20unit%20change%20in%20x%20.
# used the above formula to perform linear regression with the points as parameters to the function
def linear_line_of_best_fit(x_list, y_list):
    n = len(x_list)
    sxy = sum_helper(x_list, 1, y_list, 1) - (sum_helper(x_list, 1, [], 0) * sum_helper([], 0, y_list, 1)) / n
    sxx = sum_helper(x_list, 2, [], 0) - (sum_helper(x_list, 1, [], 0) ** 2) / n
    a = sxy / sxx
    # returned coeff to be later parsed for output by the parser function
    b = (sum_helper([], 0, y_list, 1) / n) - (a * sum_helper(x_list, 1, [], 0) / n)
    return (a, b)


# Loop through the tuple input assuming highest power coeff to lowest with size = 2 for linear or size = 3 for quadratic
# Function will return the answer as a string representing the coeff in a human readable format
def parser(vals):
    ans = ""
    exp = len(vals) - 1
    for i in vals:
        ans += "({0})x^{1}".format(i, exp)
        ans += "+"
        exp -= 1
    # We remove the last 4 characters "x^0+""
    return ans[:len(ans) - 4]


# open the input file to read the points
f = open("input.txt", "r")

# Figure out if we are doing linear or quadratic regression by reading the first line. I make sure to clean the input to accept different variations of case.
req_type = f.readline().lower().strip()
# the list to hold all the x points
x_list = []
# the list to hold all the corresponding y points
y_list = []

# the name of the file we want to write the output too
output_file_name = "output.txt"

# read all the points and append them to the correct lists by reading till the end of the file
for point in f:
    point_split = point.strip().split(",")
    if (len(point_split) != 2):
        print("points must be in the form:x,y")
    x_list.append(float(point_split[0]))
    y_list.append(float(point_split[1]))

f.close()

# if no points in file display error message
if len(x_list) == 0:
    print("must provide atleast one point, the more points the more accurate")

answer = None
# If user requested linear regression display output for it
if req_type == "linear":
    answer = parser(linear_line_of_best_fit(x_list, y_list))
    print("The linear regression output is: ", answer)

# Else if user requested quadratic regression display output for it
elif req_type == "quadratic":
    answer = parser(quadratic_regression(x_list, y_list))
    print("The quadratic regression output is: ", answer)

# Else user made an invalid request so we display an error message
else:
    print("You must request either linear or quadratic! You requested:" + req_type)

# check if we have output to write to the file
if answer is not None:
    # write to the user specified file
    f = open(output_file_name, "w")
    f.write(answer)
    f.close()