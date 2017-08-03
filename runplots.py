import weather
import keys
import plots
import datetime
import pandas as pd
import GET_A_GRIB as GAG

# inputs
#   get_weather_around_loc: extend, incr (how far to each side of current location, and in how many steps)
#   current weather circle: number of cities to catch
#   bbox: top, bottom, left, right, zoom



# get current weather
w = weather.fromDarkskyAPI().get_weather_at_loc(keys.key, 'ip')

# pygal plots
plots.show_windspeed(w, 'windspeed')
plots.show_temp_overday(w, 'temp_overday')
plots.show_temp_overdays(w, 'temp_overdays')
plots.show_winddir_overday(w, 'windbearing_radar','windbearing_line')
plots.show_rain_overdays(w, 'rain')
plots.show_temperature(w, 'temp_now')

# plotly plots
plots.webready_plotly_winddir(w)

# weather summaries
plots.weathersummaries(w)

#generate grid and save to dataframe
grid = weather.fromDarkskyAPI().get_weather_around_loc(4,8,keys.key, True, False)

time = []
for i in grid['time']:
    time.append(datetime.datetime.fromtimestamp(i).strftime('%d-%H'))

grid['time_2'] = time
df = pd.DataFrame.from_dict(grid,orient = 'index').T.to_csv('windgrid.csv', index = False)


#fire up fromOpenAPI
g = weather.fromOpenAPI(keys.key2)

curcir = g.CurrentWeatherCircle(weather.get_loc_by_ip()[0],weather.get_loc_by_ip()[1], 50)
bbox = g.CurrentWeatherBbox(8,13,54,58,10)

weather.csvFunctions().toCSV(curcir,'./data/curcir.csv', 'circle')
weather.csvFunctions().toCSV(bbox, './data/bbox.csv','bbox')

#folium plots
plots.folium_cityweather('./data/bbox.csv','./plots/bbox.html')


# getting GRIB data
for i in ['WIND,AIRTMP','WAVES']:
    filename = GAG.getMailWrapper(user, pwd, 5, 80, -70,50, timestring = '00', params = i, inc = 0.5, send = True)
    test = GAG.GRIBtoDict(filename,  delete_original = False)
    pd.DataFrame.from_dict(test[0]).to_csv('./data/{}.csv'.format(i))
    time.sleep(180)


# something something ... run the R script
#import subprocess
#subprocess.call (["/usr/bin/Rscript", "--vanilla", "/pathto/MyrScript.r"])
#import subprocess
#subprocess.check_call(['Rscript', 'vectorfield.R'], shell=False)
