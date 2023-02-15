import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def main():
	st.title('Monte Carlo Simulation for Manufacturing')
	st.info('This simulation assumes some variables follow a normal distribution.  Other variables are decided by management and are static values. \n \
		Please enter the values of the following variables and then click the run simulation button.')
	st.info('- Brandon Johnson')

	st.subheader('Static Variables')

	events = st.number_input('Enter the number of events in this simulation', value=500_000, step=10_000)

	st.write(f'Current events to simulate: {events:,}')

	quantity_produced = st.number_input('Enter the quantity to produce', value=40_000, step=100)
	st.write(f'Current quantity to produced: {quantity_produced:,}')

	unit_price = st.number_input('Enter the unit price to be sold at', value=45., step=0.5)
	st.write(f'Current unit price to be sold at: ${unit_price:,}')

	st.subheader('Normally Distributed Variables')

	
	demand_mean = st.number_input('Enter the average demand. (Units Sold)', value=50_000, step=1_000)
	st.write(f'Current demand average: {demand_mean:,}')

	demand_sd = st.number_input('Enter the standard deviation of demand', value=5000, step=100)
	st.write(f'Current demand standard deviation: {demand_sd:,}')

	

	fixed_cost_mean = st.number_input('Enter the the fixed cost average', value=10_000, step=1_000)
	st.write(f'Current fixed Cost average: ${fixed_cost_mean:,}')

	fixed_cost_sd = st.number_input('Enter the the fixed cost standard deviation', value=1_000, step=1_000)
	st.write(f'Current fixed standard deviation: ${fixed_cost_sd:,}')

	unit_cost_mean = st.number_input('Enter the unit cost to produce average', value=25., step=0.5)
	st.write(f'Current unit cost to produce average: ${unit_cost_mean:,}')

	unit_cost_sd = st.number_input('Enter the unit cost to produce standard deviation', value=3., step=0.5)
	st.write(f'Current unit cost to produce standard deviation: ${unit_cost_sd:,}')

	st.subheader('Risk Assessment')

	risk_value = st.number_input('Enter the minimum acceptable value for profit', value=250_000, step=10_000)
	st.write(f'Current minimum acceptable value for profit: ${risk_value:,}')

	
	
	if st.button('Click to Run Simulation'):

		demand = np.random.normal(loc=demand_mean, scale=demand_sd, size=events)
		unit_cost = np.random.normal(loc=unit_cost_mean, scale=unit_cost_sd, size=events)
		fixed_cost = np.random.normal(loc=fixed_cost_mean, scale=unit_cost_sd, size=events)

		quantity_sold = np.minimum(demand,quantity_produced)
		variable_cost = quantity_produced * unit_cost
		revenue = unit_price * quantity_sold
		profits = revenue - fixed_cost - variable_cost

		profits_mean = profits.mean()
		profits_median = np.median(profits)
		profits_sd = profits.std(ddof=1)


		fig1 = plt.figure(figsize=(11,11))
		sns.histplot(data=profits)
		plt.axvline(profits_mean, c='green', lw=5, label=f'Mean: ${profits_mean:,.2f}')
		plt.axvline(profits_median, c='blue', label=f'Median: ${profits_median:,.2f}')
		plt.axvline(profits_mean+profits_sd, c='orange',ls='--', label=f'+1SD: ${profits_mean+profits_sd:,.2f}')
		plt.axvline(profits_mean-profits_sd, c='orange',ls='--', label=f'-1SD: ${profits_mean-profits_sd:,.2f}')
		plt.axvline(profits_mean+profits_sd*2, c='pink',ls='--', label=f'+2SD: ${profits_mean+profits_sd*2:,.2f}')
		plt.axvline(profits_mean-profits_sd*2, c='pink',ls='--', label=f'-2SD: ${profits_mean-profits_sd*2:,.2f}')
		plt.axvline(risk_value, c='r', ls='--',label=f'Risk Value: ${risk_value:,}')
		plt.legend(fontsize=15)
		plt.title(f'Simulation with {events:,} Events', fontsize=20)

		st.pyplot(fig1)

		st.write('**Given the assumptions are correct:**')
		st.write(f'**95% ($\\pm$ 2SD from the average) likelihood the profits will be between \\${profits_mean-profits_sd*2:,.2f} and \\${profits_mean+profits_sd*2:,.2f}**')
		st.write('')
		risk_prob = (profits<risk_value).mean()
		st.write(f'**There is a {risk_prob*100:.2f}% chance that profit will be below \\${risk_value:,}**')

if __name__ == '__main__':
	main()
