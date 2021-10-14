import twint

c = twint.Config()
c.Search = 'covid'
c.Geo = "1.3560422344290832,103.80969532214895,10km"
c.Lang = 'en'
c.Limit = '10'
c.Output = "demo.csv"

twint.run.Search(c)