import twint

c = twint.Config()
c.Search = 'covid'
#c.Geo = "Singapore"
c.Lang = 'en'
c.Limit = '10'
c.Output = "demo.csv"

twint.run.Search(c)