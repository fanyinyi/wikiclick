#!/usr/bin/python3
from model.wikidb import WikiDbConnection

class WikiModel(WikiDbConnection):

    # Page rank
    def search_log(self, **kwargs):
        try:
            self.connect()
            sql_query = "select * from test3 where date = %s order by score desc limit 0,%s"

            # Executing sql!
            self.cursor.execute(sql_query, (kwargs['date'], int(kwargs['num_to_show'])))

            # Getting records
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(e)


    # Traffic Source
    def search_traffic(self, **kwargs):
        try:
            self.connect()

            date_receive = kwargs['date']
            date_post = date_receive.replace("-", "")

            sql_query ="select date, prev_title, n from rawdata" + date_post + " where curr_title=%s order by n desc limit %s"

            # Executing sql!
            self.cursor.execute(sql_query, (kwargs['page_title'],int(kwargs['num_to_show'])))

            # Getting records
            results = self.cursor.fetchall()

            return results
        except Exception as e:
            print(e)

    # Traffic To
    def search_trafficto(self, **kwargs):
        try:
            self.connect()

            date_receive = kwargs['date']
            date_post = date_receive.replace("-", "")

            sql_query = "select date, curr_title, n from rawdata" + date_post + " where prev_title=%s order by n desc limit %s"

            # Executing sql!
            self.cursor.execute(sql_query, (kwargs['page_title'], int(kwargs['num_to_show'])))

            # Getting records
            results = self.cursor.fetchall()

            return results
        except Exception as e:
            print(e)

    # Path
    def search_path(self, **kwargs):
        self.connect()
        try:
            date_receive = kwargs['date']
            date_post = date_receive.replace("-", "")
            tablename = "rawdata"+date_post
            sql_query = "select * from "+tablename+" order by n desc limit 1"
            print(sql_query)

            # Executing sql!
            self.cursor.execute(sql_query)

            # Getting records
            results = self.cursor.fetchall()
            n = 0
            oldprev = 0
            oldcurr = 0
            date = 0
            for x in results:
                n = "'"+str(x['n'])+"'"
                oldprev = "'"+x['prev_title']+"'"
                oldcurr = "'"+x['curr_title']+"'"
                date = "'"+x['date']+"'"

            sql_query2 = "insert into example1(prev_title,curr_title,n,date) values("+oldprev+","+oldcurr+","+n+","+date+")"

            self.cursor.execute(sql_query2)
            self.conn.commit()

        except Exception as e:
            print(e)

        hascycle = False
        holder = set()
        holder.add(oldprev)
        holder.add(oldcurr)

        # To determine when the path should be over
        while hascycle is False:
            try:
                sql_query3 = "select * from "+tablename+" where prev_title ="+oldcurr+" order by n desc limit 1"

                # Executing sql!
                self.cursor.execute(sql_query3)

                # Getting records
                results2 = self.cursor.fetchall()

                newprev = 0
                newcurr = 0

                for y in results2:
                    newdate = "'" + y['date'] + "'"
                    newprev = "'" + y['prev_title'] + "'"
                    newcurr = "'" + y['curr_title'] + "'"
                    newn = "'"+str(y['n'])+"'"

                if newcurr in holder:
                    hascycle = True

                else:
                    holder.add(newcurr)

                sql_query4 = "insert into example1(prev_title,curr_title,n,date) values(" + newprev + "," + newcurr + "," + newn + "," + newdate + ")"

                self.cursor.execute(sql_query4)
                self.conn.commit()

            except Exception as e:
                print(e)

            oldcurr = newcurr

        # Getting the results we want to focus on
        sql_query_final = "select prev_title, n from example1"
        self.cursor.execute(sql_query_final)

        # Getting records
        results_final = self.cursor.fetchall()
        cleanup = "truncate example1"
        self.cursor.execute(cleanup)
        self.cursor.close()
        self.conn.close()

        flowchart_code = ""
        for index, result in enumerate(results_final):
            flowchart_code += "op" + str(index) + "=>operation: " + result["prev_title"] + "\\n"

        flowchart_code += "->".join(["op" + str(index) for index in range(len(results_final))])

        return flowchart_code


