# 💰 Comprehensive Dividend Investment Calculator

A powerful, AI-assisted dividend investment calculator with global market support and comprehensive tax estimation capabilities. Built with Streamlit and Python, this tool helps investors project long-term dividend investment returns while accounting for international tax implications.

## 🌟 Features

### Core Capabilities
- **Automatic Stock Data Fetching**: Retrieves real-time price, dividend yield, and historical data via Yahoo Finance
- **Global Market Support**: Compatible with stocks from 45+ countries across major exchanges
- **Historical Analysis**: Calculates 5-year CAGR for both dividend growth and price appreciation
- **DRIP Support**: Toggle dividend reinvestment on/off to compare strategies
- **Tax Estimation**: Two-layer tax system (withholding + domestic) for 45+ countries
- **Multiple Investment Frequencies**: Support for monthly, quarterly, and annual investments
- **Comprehensive Projections**: Up to 50-year investment horizon simulations

### Visualization & Reporting
- **Interactive Charts**: Portfolio value, share accumulation, dividend income, and tax breakdown
- **Year-by-Year Breakdown**: Detailed annual summary table
- **CSV Export**: Download complete results for further analysis
- **Real-time Metrics**: CAGR, total returns, tax efficiency, and more

### Supported Markets
- **United States**: NYSE, NASDAQ (e.g., AAPL, MSFT, JNJ)
- **Canada**: TSX (add .TO, e.g., RY.TO)
- **United Kingdom**: LSE (add .L, e.g., BP.L)
- **Europe**: Multiple exchanges (e.g., SAP.DE for Germany, MC.PA for France)
- **Asia**: Hong Kong, Japan, Singapore, and more
- **Australia**: ASX (add .AX, e.g., BHP.AX)
- And many more!

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd dividend-calculator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   You should see `(venv)` at the start of your command prompt.

4. **Install required packages**
   ```bash
   pip install streamlit yfinance pandas numpy plotly
   ```
   
   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Navigate to the project directory**
   ```bash
   cd /path/to/your/dividend-calculator
   ```

2. **Start the Streamlit app**
   ```bash
   streamlit run dividend_calculator.py
   ```

3. **Access the application**
   - The app will automatically open in your default web browser
   - If not, navigate to `http://localhost:8501`

## 📖 How to Use

### Step 1: Enter Stock Information
1. Enter a stock ticker symbol in the sidebar (e.g., AAPL, MSFT, VOO)
2. Click "Fetch Stock Data" to retrieve current information
3. Review auto-populated data:
   - Current price and dividend yield
   - Annual dividend rate
   - Historical growth rates (5-year CAGR)
   - Detected dividend frequency
   - Stock country/exchange

### Step 2: Configure Investment Parameters
- **Initial Investment**: Starting capital amount
- **Additional Investment**: Regular contribution amount
- **Frequency**: Monthly, quarterly, or annual contributions
- **Investment Period**: 1-50 years
- **DRIP**: Enable/disable dividend reinvestment

### Step 3: Set Growth Assumptions
- **Dividend Growth Rate**: Expected annual dividend increase (auto-filled with historical data)
- **Price Growth Rate**: Expected annual stock price appreciation (auto-filled with historical data)
- **Dividend Frequency**: How often dividends are paid (auto-detected)

### Step 4: Configure Tax Settings
1. Select your country (investor location)
2. Review the auto-detected stock country
3. View default tax rates:
   - Withholding tax (applied at source)
   - Domestic tax (applied in your country)
4. Override rates if needed for your specific situation

### Step 5: Calculate & Analyze
- Click "Calculate Investment Projection"
- Review comprehensive results:
  - Investment summary metrics
  - Interactive charts
  - Year-by-year breakdown table
  - Download CSV for detailed analysis

## 🌍 Tax Calculation System

The calculator implements a realistic two-layer tax system:

1. **Withholding Tax**: Applied by the country where the stock is listed
2. **Domestic Tax**: Applied by your country on net dividends received

### Example
A Trinidad & Tobago investor in US stocks:
- 30% US withholding tax (or 15% with tax treaty)
- 10% Trinidad domestic tax on remaining amount
- Effective combined tax rate displayed

### Supported Countries (45+)
United States, Canada, United Kingdom, Germany, France, Australia, Japan, Singapore, Trinidad and Tobago, India, China, Brazil, South Africa, Mexico, Netherlands, Switzerland, Sweden, Spain, Italy, South Korea, Hong Kong, New Zealand, Ireland, Belgium, Austria, Denmark, Norway, Finland, Poland, Portugal, Greece, Turkey, Thailand, Malaysia, Philippines, Indonesia, Vietnam, Chile, Argentina, Colombia, Peru, Israel, Saudi Arabia, UAE, Egypt, Nigeria, Kenya, Pakistan, Bangladesh

## 🎯 Key Features Explained

### DRIP (Dividend Reinvestment Plan)
- **Enabled**: Net dividends automatically purchase additional shares
- **Disabled**: Dividends accumulate as cash

### CAGR Calculation
Compound Annual Growth Rate is calculated for:
- Historical dividend growth (5-year)
- Historical price appreciation (5-year)
- Overall portfolio performance

### Caching System
- Stock data cached for 1 hour to minimize API calls
- Improves performance and respects API rate limits

## 📁 Project Structure

```
dividend-calculator/
│
├── dividend_calculator.py    # Main application file
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── LICENSE                  # License information
└── .gitignore              # Git ignore file
```

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **yfinance**: Stock data retrieval
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Plotly**: Interactive visualizations

### Data Sources
- Real-time stock data: Yahoo Finance
- Tax rates: Based on publicly available tax information (rates are approximations)

### Architecture
- Modular function design
- Session state management for data persistence
- Efficient caching to minimize API calls
- Responsive layout for various screen sizes

## ⚠️ Important Disclaimers

### Tax Information
- Tax calculations are **estimates for educational purposes only**
- Actual tax liability depends on:
  - Individual circumstances
  - Tax treaties between countries
  - Account type (taxable vs. retirement)
  - Current tax laws and regulations
- **Always consult with qualified tax and financial professionals**

### Investment Information
- Historical performance does not guarantee future results
- Projections are based on assumed growth rates
- Actual results may vary significantly
- This tool is for planning and educational purposes only
- Not financial advice

## 🤝 Contributing

This project was developed with AI assistance. Contributions, suggestions, and improvements are welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- Additional country tax data
- Enhanced visualization options
- Support for additional asset types (REITs, ETFs)
- Portfolio-level analysis (multiple stocks)
- Tax-loss harvesting calculations
- Currency conversion support
- Unit tests and test coverage
- Documentation improvements

## 🐛 Known Issues & Limitations

- Tax rates are approximations and may not reflect current laws
- Some international exchanges may have limited data availability
- API rate limits may affect frequent users
- Tax treaties and special agreements are not fully modeled
- Does not account for currency exchange rates

## 📝 License

This project is open source and available under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

- Built with assistance from Claude (Anthropic AI)
- Data provided by Yahoo Finance via yfinance library
- Tax rate data compiled from various public sources
- Inspired by the need for accessible international investment planning tools

## 📞 Support & Feedback

For questions, issues, or feature requests:
- Open an issue in the repository
- Check existing issues for solutions
- Contribute improvements via pull requests

## 🔄 Version History

### Version 1.0.0 (Initial Release)
- Real-time stock data fetching
- 45+ country tax support
- DRIP simulation
- Interactive visualizations
- CSV export functionality
- Comprehensive documentation

---

**Made with AI** 🤖 | **Data by Yahoo Finance** 📊 | **Educational Tool Only** 📚

---

## 📚 Additional Resources

### Learning Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Dividend Investing Basics](https://www.investopedia.com/terms/d/dividend.asp)
- [International Tax Treaties](https://www.irs.gov/businesses/international-businesses/united-states-income-tax-treaties-a-to-z)

### Related Projects
- Portfolio optimization tools
- Stock screening applications
- Tax optimization calculators
- Financial planning software

---

**Last Updated**: November 2025