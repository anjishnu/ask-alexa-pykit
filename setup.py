from distutils.core import setup

setup(name='ask-alexa-pykit',
      version='0.5.6',
      description="Minimalist SDK for developing skills for Amazon's Alexa Skills Kit for Amazon Echo Dot Tap FireTV etc",
      author='Anjishnu Kumar',
      author_email='anjishnu.kr@gmail.com',
      url='https://github.com/anjishnu/ask-alexa-pykit',
      packages=['ask', 'ask.config'],
      keywords=['alexa', 'amazon echo', 'ask', 'ask-alexa-pykit', 'skill'],
      package_data={'ask.config': ['../data/*']},
      license='MIT',
)
