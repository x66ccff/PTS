from scipy.integrate import solve_ivp
import numpy as np
import pandas as pd
from pysindy import SmoothedFiniteDifference

def gen_phy_data(func, bound_t_ls, n_t, x_0_ls, x_names, xdots_names, deriv_idxs):
    assert len(xdots_names) == len(deriv_idxs)
    assert type(bound_t_ls) is list
    assert type(x_0_ls) is list
    assert type(x_names) is list
    assert type(xdots_names) is list
    assert type(deriv_idxs) is list

    t_span = bound_t_ls   
    sol = solve_ivp(func, bound_t_ls, x_0_ls, dense_output=True)
    t = np.linspace(bound_t_ls[0], bound_t_ls[1], n_t)
    z = sol.sol(t)
    data = z.T.copy()
    sfd = SmoothedFiniteDifference(smoother_kws={'window_length': 5})

    data_deriv = np.zeros((data.shape[0],len(deriv_idxs)))
    for i,idx in enumerate(deriv_idxs):
        # print(data[:,idx:idx+1].shape,t.shape)
        deriv_data_i = sfd._differentiate(data[:,idx:idx+1], t)
        data_deriv[:,i:i+1] = deriv_data_i
        
    df = pd.DataFrame(np.hstack([data, data_deriv]))
    df.columns = x_names + xdots_names
    return df

