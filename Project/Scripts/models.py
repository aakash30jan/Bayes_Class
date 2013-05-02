from __future__ import division
import numpy as np
import roth
import data
import pymc as mc

def uniform_priors():
    # Priors
    # modSig, hoc, igFac
    modSig = mc.Uniform('modSig', lower=500., upper=50000., value=2000.)
    hoc = mc.Uniform('hoc', lower=1., upper=50000., value=6000.)
    mExt = mc.Beta('mExt', alpha=2., beta=5., value=0.2)
    # mExt = mc.Uniform('mExt', lower=0., upper=1., value=0.3)
    # igFac = mc.Uniform('igFac', lower=1., upper=1000., value=100.)

    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model - switch mc and hoc
    @mc.deterministic
    def y_mean(modSig=modSig, mBulk=data.meanBulk, hoc=hoc, moistC=data.mcs, moistE=mExt):
        return roth.flameSpread(sigma=modSig, bulk=mBulk, hoc=hoc, moist=moistC, mExt=moistE)

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data.rates,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
