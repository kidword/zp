from scrapy.cmdline import execute

if __name__=="__main__":
    execute("scrapy crawl job -o job.csv".split())
    # -o 代表输出文件， -t 代表文件格式   -t 可以省略
