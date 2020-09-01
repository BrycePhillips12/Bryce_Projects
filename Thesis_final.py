import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import signal
from scipy import integrate
from scipy.integrate import simps
from numpy import trapz
import xlwings as xw

#VCONST = density*cross-section*Avogodro's #*velocity(naught)/Atomic weight
VCONST = 8.145191699

def bottom_integral(v, y):
    """ Makes a list of values for the bottom integral of equation (18) and
    then integrates it """

    vb = []
    for i in range(len(v)):
        exp = (-1) * VCONST / v[i]
        b = (y[i])  * (1 - math.exp(exp))
        vb.append(b)

    return vb


def time_transformation(v_list, d):
    """ Transforms velocity spectrum to a time of flight spectrum"""
    t_list = []
    for num in v_list:
        t_list.append(d/num)

    return t_list

def velocity_transformation(t, d):
    """ """

    trans_list = []
    for num in t:
        trans_list.append(d/num)

    return trans_list


def time_delay(t_list, y_list, final):
    """ Transforms velocity spectrum to a time of flight spectrum"""
    i = 1
    time_int = .000001
    transx_final = [0]
    transy_final = [final]
    while i < 100:
        time_list = []
        for idx in t_list:
            time_list.append(idx + (time_int * i))
        transx_list = velocity_transformation(time_list, 4)
        transy_final.append(solve(transx_list, y_list))
        transx_final.append(i*time_int)
        # if i == 99:
        #     plotter(transx_list, y_list, "Velocity (m/s)", "Capture Flux", "Capture Flux vs Velocity after Time Shift")
        i += 1

    c1 = []
    for num in transy_final:
        c1.append((num - 1)*886.3)

    min = 1
    for idx in range(len(c1)):
        if abs(c1[idx] - (c1[0] + .1)) < min:
            min = abs(c1[idx] - (c1[0] + .1))
            tenth_x = idx * .000001
            tenth_y = c1[idx]

    ylabel = 'Correction in seconds'
    xlabel = 'Time Delay (s)'
    title = 'Fission Chamber - Timing Error'
    # plotter(transx_final, c1, xlabel, ylabel, title)
    print('timing error to get a tenth of a second error', tenth_x, 's')


def dist_delay(v, y, f):
    """ """
    i = 1
    d = .001
    distx_final = [0]
    disty_final = [f]
    while i < 151:
        tx = time_transformation(v, (4 + d*i))
        distx_list = velocity_transformation(tx, 4)
        disty_final.append(solve(distx_list, y))
        distx_final.append(d*i)
        # if i == 150:
        #     plotter(distx_list, y, "Velocity (m/s)", "Capture Flux", "Capture Flux vs Velocity after Distance Shift")
        i += 1

    c1 = []
    for num in disty_final:
        c1.append((num - 1)*886.3)

    min = .1
    for idx in range(len(c1)):
        if abs(c1[idx] - (c1[0] + .1)) < min:
            min = abs(c1[idx] - (c1[0] + .1))
            tenth_x = idx * .001
            tenth_y = c1[idx]

    ylabel = 'Correction in seconds'
    xlabel = 'Distance Error (m)'
    title = 'Fission Chamber - Distance Correction'
    # plotter(distx_final, c1, xlabel, ylabel, title)
    print('distance error to get a tenth of a second error', tenth_x, 'm')


def solve(x, y):
    """Solves the equation for the c1 term
    given an unweighted velocity spectrum"""

    # Making a list of values inside the bottom integral of eq 2
    # bottom_integral returns (1-e^(k/v)) values where k is constant
    bot_list = bottom_integral(x, y)
    # The top integral has an extra 1/v term in it so the weighting does that
    weighted = []
    for i in range(len(y)):
        weighted.append(y[i]/x[i])
    # integrating the top integral of eq 2
    top_int = integrate.simps(weighted, x)
    # integrating the bottom integral of eq 2
    bot_int = integrate.simps(bot_list, x)
    # Multiple the top integral by the constants to get the value of the numerator
    top_expr = VCONST * top_int
    # Numerator / Denominator gives the value of c1
    final = top_expr / bot_int

    return final


def plotter(x, y, xlabel, ylabel, title):
    """ """

    plt.plot(x, y)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    # plt.scatter(tenth_x, tenth_y, s = 10)
    plt.show()


def convolute(t_list, y_list, normal):
    """ """
    convoluted = []
    cx = []
    for j in range(1, 200):
        line = signal.triang(j*10)
        conv = signal.convolve(normal, line, 'same') / sum(line)
        v_list = velocity_transformation(t_list, 4)
        unnormal = []
        for idx in range(len(conv)):
            unnormal.append(conv[idx]*t_list[idx])
        convoluted.append(solve(v_list, unnormal))
        cx.append(t_list[len(t_list) - j*10] / 2)
        # if j == 50:
        #     plotter(v_list, unnormal, "Velocity (m/s)", "Capture Flux", "Capture Flux vs Velocity after Convolution")


    c1 = []
    for num in convoluted:
        c1.append((num - 1)*886.3)

    min = .1
    for idx in range(len(c1)):
        if abs(c1[idx] - (c1[0] + .1)) < min:
            min = abs(c1[idx] - (c1[0] + .1))
            tenth_x = cx[idx]
            tenth_y = c1[idx]

    xlabel = 'Width of Triangle Signal (s)'
    ylabel = 'Correction in Seconds'
    title = 'Correction Dependence on Convolution to Triangle Signal'
    print('Width of Triangle Signal to get a tenth of a second error', tenth_x, 's')
    # plotter(cx, c1, xlabel, ylabel, title)


def time_weight(t, y, f):
    """ """
    timex_final = [0]
    timey_final = [f]
    for i in range(100, 300):
        weighted = []
        x = 1 + (i * .0001)
        for idx in range(len(t)):
            weighted.append(t[idx] * (x))
        v = velocity_transformation(weighted, 4)
        timey_final.append(solve(v, y))
        timex_final.append((x-1)*100)
        # if i == 299:
        #     plotter(v, y, "Velocity (m/s)", "Capture Flux", "Capture Flux vs Velocity after Time Weight")

    c1 = []
    for num in timey_final:
        c1.append((num - 1)*886.3)

    min = .1
    for idx in range(len(c1)):
        if abs(c1[idx] - (c1[0] + .1)) < min:
            min = abs(c1[idx] - (c1[0] + .1))
            tenth_x = timex_final[idx]
            tenth_y = c1[idx]

    xlabel = 'Percent Deviation in Timing'
    ylabel = 'Correction in seconds'
    title = 'Correction Dependence on Time Weighting'
    print('Timing error to get a tenth of a second error',tenth_x,'%')
    # plotter(timex_final, c1, xlabel, ylabel, title)


def main():
    # wb is the excel workbook
    wb = xw.Book('Best_data.xlsx')
    # sht is the sheet name of that workbook
    sht = wb.sheets('FC')

    # vy_list takes a column with values I(v) / v, where I(v) is intensity given
    # velocity. vx_list takes the column of velocities corresponding to vy_list.
    # Note that vx_list must be in ascending order.
    y_list = sht.range('G2:G9850').value
    v_list = sht.range('F2:F9850').value
    wavelength = sht.range('A2:A9850').value
    # 9850

    final = solve(v_list, y_list)
    print("c1 (total) =", final)

    # Transforming velocity spectrum to ToF spectrum

    # ***figure out what's good with time spectrum***
    t_list = time_transformation(v_list, 4)

    # plotter(wavelength, y_list, "Wavelength (Angstrom)", "Capture Flux", "Capture Flux vs Wavelength")
    #
    # plotter(t_list, y_list, "Time (s)", "Capture Flux", "Capture Flux vs Time")
    #
    # plt.plot(v_list, y_list)
    time_delay(t_list, y_list, final)
    # plt.plot(v_list, y_list)
    dist_delay(v_list, y_list, final)
    # plt.plot(v_list, y_list)
    time_weight(t_list, y_list, final)

    # plt.plot(v_list, y_list)
    # plt.show()
    # plt.plot(t_list, y_list)
    # plt.show()
    # plt.plot(y_list)
    # plt.show()

    normal = []
    for idx in range(len(y_list)):
        normal.append(y_list[idx] / t_list[idx])
    # plt.plot(v_list, y_list)
    convolute(t_list, y_list, normal)

    #resample before convolution


if __name__ == '__main__':
    main()
