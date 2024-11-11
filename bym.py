# required libraries
import requests
import argparse
import sys
import os.path
import time
import random

#bym -u URL
#    -w WORDLIST 
#    -f FILE (jpg,xml,exe,db)
#    -t TIMEOUT (timeout between requests) R = random
#    -h HEADER FILE
#    -o OUTPUT FILE


#response = requests.get("https://host.com")

#if (response.status_code == 200):
#    print ('success!')
#    index_page = response.content
#    print (index_page)





# error message
def program_usage(error_message):
    print ('usage: bym [-h] [-u URL] [-w WORDLIST] [-f FILES] [-t DELAY]')
    print ('[-u http://target.com] [-w /home/johndoe/wordlist.txt] [-o /home/johndoe/report.txt]')
    print ('-f jpg,bmp,sql,xml,db,bkp] [-t 1-10 or R]')
    if (error_message == ''):
        print ('')
    else:
        print ('warning: ' + error_message)


# verify and remove / from URL
def remove_bar(bURL):
    size_url = len(bURL)
    last_char = bURL[size_url - 1]

    if (last_char == '/'):
        return bURL[:-1]
    else:
        return bURL

# file output function
def write_log(file_path, line_content):
    try:
        with open(file_path, 'a+') as write_line:
            write_line.write(line_content)
        write_line.close()
    except Exception as e:
        print (e)


# make a HTTP request
def http_request_response(hRequest, hHeaders):
    try:
        hResponse = requests.get(hRequest, headers=hHeaders)

        # verify if HTTP response is on the status code list
        if hResponse.status_code in status_code_list:
            if (hResponse.status_code == 200):
                hDescription = 'OK'
            elif (hResponse.status_code == 202):
                hDescription = 'Accepted'
            elif (hResponse.status_code == 301):
                hDescription = 'Move Permanently'
            elif (hResponse.status_code == 302):
                hDescription = 'Move Temporarily'
            elif (hResponse.status_code == 401):
                hDecription = 'Unauthorized'
            
            if (hRequest[-1:] == '/'):
                hReturn = '[+]  ' + hRequest[:-1] + '\t' + hDescription
            else:
                hReturn = '[+]  ' + hRequest + '\t' + hDescription
            return hReturn
        else:
            pass
    except:
        print ('[-] connection error, quiting.')
        sys.exit()




# pre load configuration
def scanning():


    print ('\n\n\t██████╗ ██╗   ██╗███╗   ███╗    ███████╗ ██████╗ █████╗ ███╗   ██╗')
    print ('\t██╔══██╗╚██╗ ██╔╝████╗ ████║    ██╔════╝██╔════╝██╔══██╗████╗  ██║')
    print ('\t██████╔╝ ╚████╔╝ ██╔████╔██║    ███████╗██║     ███████║██╔██╗ ██║')
    print ('\t██╔══██╗  ╚██╔╝  ██║╚██╔╝██║    ╚════██║██║     ██╔══██║██║╚██╗██║')
    print ('\t██████╔╝   ██║   ██║ ╚═╝ ██║    ███████║╚██████╗██║  ██║██║ ╚████║')
    print ('\t╚═════╝    ╚═╝   ╚═╝     ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝\n\n')

    # print target detail
    print ('>>> Target: ' + str(args.target_url))
    

    # check wordlist and set default if is not set
    if (args.target_wordlist == None):
        args.target_wordlist = 'database/default.txt'
    else:
        if (os.path.isfile(args.target_wordlist)):
            pass
        else:
            print ('warning:' + args.target_wordlist + ' file not exists, please specify a valid path.')

    # print selected wordlist
    print ('>>> Wordlist: ' + str(args.target_wordlist))

    print ('\n')

    # http request header configuration
    # user-agent list: 
        # Mozilla/5.0 (X11; Linux x86_64)
        # AppleWebKit/537.36 (KHTML, like Gecko) 
        # Chrome/56.0.2924.87 
        # Safari/537.36
    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }



    # open wordlist file
    with open(args.target_wordlist, 'r') as f:
        # read content
        wordlist_content = f.readlines()
        # read it line by line
        for i in range(0, len(wordlist_content)):
            # create URL + wordlist line
            gURL = args.target_url + '/' + wordlist_content[i]

            # config delay between connections
            if (args.target_delay == None):
                args.target_delay = 1
            elif (args.target_delay == 'R'):
                args.target_delay = random.choice(random_delay)
            else:
                args.target_delay = int(args.target_delay)

            time.sleep(args.target_delay)
            
            # make a request
            response = http_request_response(gURL, headers)
            if (response != None):
                print (response)
                # verify if output flag is turned on
                if (args.target_output != None):
                    write_log(str(args.target_output), response + '\n')


            # create and scan file extensions
            if (args.target_files != None):
                if ',' in args.target_files:
                    # slit file extension
                    split_1 = args.target_files.split(',',)
                    for i in range(0, len(split_1)):
                        newgURL = gURL[:-1] + '.' + split_1[i]
                        # make a request
                        response = http_request_response(newgURL, headers)
                        if (response != None):
                            print (response)
                            # verify if output flag is turned on
                            if (args.target_output != None):
                                write_log(str(args.target_output), response + '\n')

                # one extension only                      
                #else:
                #    file_extension = split_1[i]
                #    gURL = args.target_url + '/' + wordlist_content[i] + '.' + [1:]args.target_files
                #    # make a request
                #    response = http_request_response(gURL, headers)
                #    if (response != None):
                #        print (response)
                #        # verify if output flag is turned on
                #        if (args.target_output != None):
                #            write_log(str(args.target_output), response + '\n')                    



# main function
def main():                                                       
                            
    # global variables
    global args
    global random_delay
    global status_code_list
    global file_extensions

    # set variables values
    random_delay = [1, 1.4, 1.8, 2, 2.1, 2.2, 3, 3.1, 3.4, 5, 7]

    # 200 - OK
    # 202 - Accepted
    # 301 - Move Permanently
    # 302 - Found (Previously "Move Temporarily")
    # 401 - Unauthorized
    status_code_list = [200, 202, 301, 302, 401]

    # argument list
    parser = argparse.ArgumentParser(description='Bym Web Scanner - created by Mil3tus')
    parser.add_argument('-u', dest='target_url', type=str, metavar='<URL>',
                        help='-u http://target.com\t')
    parser.add_argument('-w', dest='target_wordlist', type=str, metavar='<PATH>',
                            help='-w /home/johndoe/wordlist.txt')
    parser.add_argument('-f', dest='target_files', type=str, metavar='File extensions',
                            help='-f jpg,php,sql,db')
    parser.add_argument('-o', dest='target_output', type=str, metavar='Output file',
                            help='-o /home/johndoe/report.txt')
    parser.add_argument('-t', dest='target_delay', type=str, metavar='Delay between requests',
                            help='-t (0.1-10) or R (random)\n')
    args = parser.parse_args()


    # verify argument list
    if not len(sys.argv[1:]):
        program_usage('')
    else:
        if (args.target_url != None):
            # verify if user insert a / in the end of URL
            args.target_url = remove_bar(args.target_url)
            
            # pre load configurations to start scanning
            scanning()

    

main()