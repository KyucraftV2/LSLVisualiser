
fname = "./test.xdf"
streams, header = pyxdf.load_xdf(fname)
data = streams[0]["time_series"]
print(len(streams[1]))
for stream in streams[1] :
    print(stream)

print(streams[1]["time_stamps"])
y = []
for test in streams[1]["time_series"] :
    y.append(test)
print(streams[1]["time_series"])
plt.plot(streams[1]["time_stamps"], y)
plt.show()
