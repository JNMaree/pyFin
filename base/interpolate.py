

# Linear Interpolation function\n",
#   - assumes x & y are sorted, correlated lists/np.arrays\n",
def lerp(x_list,y_list,xs) -> float:
    ct = 0
    while xs > x_list[ct] and ct < len(x_list):
        ct += 1
    return y_list[ct-1] + (xs - x_list[ct-1])*(y_list[ct]-y_list[ct-1])/(x_list[ct]-x_list[ct-1])