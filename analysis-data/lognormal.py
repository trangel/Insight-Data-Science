# Define lognormal distribution
def lognormal(x, sigma,mu):
    import numpy as np
    from math import sqrt, pi
    eta=0.001
    p = 1.0/(x*sigma*sqrt(2.0*pi)+eta)
    c=(np.log(x+eta)-mu)**2/(2.0*sigma**2+eta)
    ff=p*np.exp(-1.0*c)
    return ff

def lognormal_stats(sigma,mu):
    from math import exp
    mean=exp(mu+sigma**2/2.0)
    variance=(exp(sigma**2)-1.0)*exp(2.0*mu+sigma**2)
    return mean,variance

# Define decaying exp.
def truncated_normal(x, sigma,mu):
    import numpy as np
    from math import sqrt, pi
    xmin=0
    f1=1.0/(sqrt(2.0*pi*sigma**2))
    f2=np.exp(-(x-mu)**2/(2*sigma**2))
    ff=f1*f2
    for ii in range(len(ff)):
        if ff[ii] < xmin:
            ff[ii]=0 
    return ff

