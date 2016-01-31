import numpy as np
import pymc3 as pm
import scipy as sp
import pymc3 as pm
import pickle
import matplotlib.pyplot as plt
import pylab as pl
import ipdb

from collections import defaultdict

def run_ppc(trace, samples=100, model=None):
    """Generate Posterior Predictive samples from a model given a trace.
    """
    if model is None:
         model = pm.modelcontext(model)

    ppc = defaultdict(list)
    for idx in np.random.randint(0, len(trace), samples):
        param = trace[idx]
        for obs in model.observed_RVs:
            ppc[obs.name].append(round(obs.distribution.random(point=param)))

    return ppc

model = pm.Model()

# This model approximates the avg time spent per session as a distribution
observed_numberOccurrences = pickle.load( open( "numberOccurrence.p", "rb" ) )
# observed_ipFrequencies = pickle.load( open( "ipBinaryFrequency.p", "rb" ) )

weekend_timeStart_observed = pickle.load(open("weekendStartShort.p", "rb"))
# pickle.dump(weekend_timeStart_observed[:1000000], open("weekendStartShort.p", "wb"))
weekday_timeStart_observed = pickle.load(open("weekdayStartShort.p", "rb"))
# pickle.dump(weekday_timeStart_observed[:1000000], open("weekdayStartShort.p", "wb"))
a_observed = np.array(weekend_timeStart_observed)
b_observed = np.array(weekday_timeStart_observed)

# n_bins = 24
# n, bins, patches = plt.hist(b, n_bins, normed = 1,
#                             histtype='bar')
# plt.title("Weekend Start Time Hour Distribution")
# plt.show()


# n_bins = 24
# n, bins, patches = plt.hist(c, n_bins, normed = 1,
#                             histtype='bar')
# plt.title("Weekday Start Time Hour Distribution")
# plt.show()


# # observed_timeFrequencies = pickle.load( open( "TimeBinaryFrequency.p", "rb" ))
# dow = pickle.load( open( "dayOfWeek.p", "rb" ))
# b = np.array(dow)
# c = []

# for item in b:
#     c.append(float(item) / sum(b))

# print b
# labels = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
# plt.bar([1,2,3,4,5,6,7],c, align = 'center')
# plt.xticks([1,2,3,4,5,6,7], labels)

# plt.title("Day Of Week Distribution")
# plt.show()

# print sp.stats.describe(b)
# print b
# y = np.bincount(b)
# print y
# # lower_bound = np.percentile(b, 2)
# # b = filter(lambda x: x >= lower_bound, b)
# n, bins, patches = plt.hist(b, bins=[0,1,2,3,4,5,6,7], normed = 1,
#                             histtype='bar')
# plt.title("Day Of Week Distribution")
# plt.show()


# tod = pickle.load( open( "timeOfDay.p", "rb" ))
# b = np.array(tod)
# print sp.stats.describe(b)
# # lower_bound = np.percentile(b, 2)
# # b = filter(lambda x: x >= lower_bound, b)
# n_bins = 24
# n, bins, patches = plt.hist(b, n_bins, normed = 1,
#                             histtype='bar')
# plt.title("Start Time Hour Distribution")
# plt.show()

# print observed_ipFrequencies

# plt.plot(observed_timeFrequencies, 'ro')
# plt.show()


# a = np.array(observed_numberOccurrences)
# upper_bound = np.percentile(a, 95)
# lower_bound = np.percentile(a, 5)
# a = filter(lambda x: x <= upper_bound, observed_numberOccurrences)
# a = filter(lambda x: x >= lower_bound, a)

# observed_numberOccurrences = filter((lambda x: x < 200), observed_numberOccurrences)
# n_bins = 50
# n, bins, patches = plt.hist(a, n_bins, normed=1,
#                             histtype='step')
# plt.show()
# weekend_observed = []


with model: # model specifications in PyMC3 are wrapped in a with-statement



    # define priors
    muA = pm.Uniform('muA', lower=0, upper=24)
    muB = pm.Uniform('muB', lower=0, upper=24)
    muC = pm.Uniform('muC', lower=0, upper=24)

    sigmaA = pm.Uniform('sigmaA', lower=0, upper=1000)
    sigmaB = pm.Uniform('sigmaB', lower=0, upper=1000)
    sigmaC = pm.Uniform('sigmaC', lower=0, upper=1000)


    distributionA = pm.Normal('a', mu = muA, sd = sigmaA, observed = a_observed)
    # distributionB = pm.Normal('b', mu = muB, sd = sigmaB, observed = b_observed)
    # distributionC = pm.Normal('c', mu = muC, sd = sigmaC, observed = c_observed)

    x1 = pm.Uniform('x1', lower = -10000, upper = 10000)
    x2 = pm.Uniform('x2', lower = -10000, upper = 10000)
    t1 = pm.Uniform('t1', lower = -10000, upper = 10000)
    t2 = pm.Uniform('t2', lower = -10000, upper = 10000)
    

    def distributionB(value = b_observed, mu = muA, x1 = x1, sigma = sigmaA, x2= x2, t1 = t1, t2= t2):
        return pm.Normal('b', mu = mu * x1 + x2, sd = sigma * t1 + t2, observed = value)

    # b_model = pm.Deterministic('b_model', model=distributionB)

    ipdb.set_trace()
    distributionB = distributionB()

    
    # @pm.observed
    # def Z(value=b_observed, mu=muA, tau=tau_A, y=bb):
    #     # Likelihood for x (also latent, but fixed given y and z)
    #     return pm.normal_like(value-y, mu, tau)

     
    # muB = pm.Lambda('p_B', lambda R=R: pl.where(distributionA, .5, .8),
    #             doc='Pr[B|A]')
    # B = pm.Bernoulli('S', p_S, value=pl.ones(N))
 
    # p_C = pm.Lambda('p_C', lambda A=A, B=B:
    #             pl.where(S, pl.where(R, .99, .9), pl.where(R, .8, 0.)),
    #             doc='Pr[C|A,B]')

    start = pm.find_MAP()
    step = pm.Slice()

    niter = 100
    trace = pm.sample(niter, step, start, progressbar=True)

    pm.traceplot(trace, vars=['muA'])
    plt.show()

    # # print ppc['Y_obs']
    # print ppc['distributionA']
    # print ppc['distributionB']
    # tau = pm.Uniform('tau', lower=0, upper=1000)
    # lam = pm.Uniform('lam', lower = 0, upper = 1000)
    # alpha = pm.Uniform('alpha', lower = 0.0000000000000001, upper = 100)
    
    # p_weekend = float(len(b)) / (len(b) + len(c))
    # print "Got here"
    # # weekend = pm.Bernoulli('weekend', p_weekend, observed = weekend_observed)
    # print b[:3000]
    # print c[:3000]
    # startTimeWeekend = pm.Normal('a', mu = muA, sd = sigmaA, observed = b[:30000])
    # startTimeWeekday = pm.Normal('b', mu = muB, sd = sigmaB, observed = c[:30000])

    # print "Got here2"
    # # define likelihood
    # # y_obs = pm.Normal('Y_obs', mu=mu, sd=sigma, observed=observed_numberOccurrences)
    # # y_obs = pm.Lognormal("Y_obs", mu = mu, tau = tau, observed = a)
    # # y_obs = pm.Exponential("Y_obs", lam = lam, observed = a)
    # # y_obs = pm.Pareto("Y_obs", alpha, 1, observed = a)

    # # inference
    # start = pm.find_MAP()
    # print "Got here3"
    # step = pm.Slice()
    # print "Got here4"
    # niter = 500
    # trace = pm.sample(niter, step, start, progressbar=True)
    # print "Got here5"
    # ppc = run_ppc(trace, model=model, samples=200)

    # # print ppc['Y_obs']
    # print ppc['startWeekend']
    # print ppc['startWeekday']



    pm.summary(trace)
    # # Define random variables
    # theta_a = pm.Normal('theta_a', mu=15, sd=5) # prior
    # theta_b = pm.Normal('theta_b', mu=15, sd=5) # prior
    
    # # Define how data relates to unknown causes
    # data_a = pm.Normal('observed A',
    #                       p=theta_a, 
    #                       observed=algo_a)
    
    # data_b = pm.Normal('observed B', 
    #                       p=theta_b, 
    #                       observed=algo_b)
    
    # # Inference!
    # start = pm.find_MAP() # Find good starting point
    # step = pm.Slice() # Instantiate MCMC sampling algorithm
    # trace = pm.sample(10000, step, start=start, progressbar=False) # draw posterior samples using slice sampling 