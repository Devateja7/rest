from flask import Flask,jsonify,Blueprint
from flask_restplus import Api,Resource,fields,cors
from flask_pymongo import PyMongo
from flask_cors import CORS
from collections import defaultdict
app = Flask(__name__)
api = Api(app)
cors = CORS(app)
# CORS(app, origins="*", allow_headers=[
#     "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
#     supports_credentials=True)

app.config["MONGO_URI"] = "mongodb://localhost:27017/imdbb"
mongo = PyMongo(app)
obj = mongo.db.movies
model1 = api.model('movies1',{'99popularity':fields.Integer,'director':fields.String,
                            'genre':fields.List(fields.String),'imdb_score':fields.Float,
                            'name':fields.String})

model2 = api.model('NameModel', 
		  {'director': fields.String(required = True)})
# model2 = api.model('movies2',{'99popularity':fields.Integer,'director':fields.String,'genre':fields.List,
#                             'imdb_score':fields.Float,'name':fields.String})
ns_movies = api.namespace('movie', description = "movie_details")

ms_movies = api.namespace('search',description = "movie_details")


@api.route('/movies')
class total(Resource):
    # @cors.crossdomain(origin='*')
    def get(self):
        d = obj.find()
        result = []
        for i in d:
            dic ={}
            dic ={'99popularity' : i['99popularity'],'director': i['director'],'genre':i['genre'],'imdb_score':i['imdb_score'],'name':i['name']}
            result.append(dic)
        return jsonify(result)
    
    @api.expect(model1)
    def post(self):
        data = api.payload
        # obj.insert(data)
        # data.pop('_id')
        return {'movie_added':data}, 200, {'Access-Control-Allow-Origin': '*'}

@ms_movies.route('/')
class total(Resource):
    @api.expect(model2)
    @api.marshal_with(model1, envelope="movie_list")
    def post(self):
        # print(model1)
        data = api.payload
        print(data)

        d = obj.find({"director": data['director']})
        l = []
        for i in d:
            l.append(i)
            # print(i['director'])
        return l








@ns_movies.route('/')
class total(Resource):
    @api.marshal_with(model1, envelope="movie_list")
    def get(self):
        d = obj.find()
        result = []
        for i in d:   
            dic ={'99popularity' : i['99popularity'],'director': i['director'],
            'genre':i['genre'],'imdb_score':i['imdb_score'],'name':i['name']}
            result.append(dic)
        return result

    @api.marshal_with(model2, envelope="movie_list")
    def post(self):
        print(model2)
        data = api.payload

        d = obj.find(data)
        return d

    
     

    @api.expect(model1)
    # @cors.crossdomain(origin='*')
    # @api.marshal_with(model1, envelope="movie_added")
    def post(self):
        data = api.payload
        print(data)
        obj.insert(data)
        data.pop('_id')
        return {"msg": data}, 200

    @api.expect(model1)
    @api.marshal_with(model1, envelope="movie_updated")
    def put(self):
        data = api.payload
        obj.update_one({'99popularity' : data['99popularity']},{"$set":{'director': data['director']}})
        return data



        

# @api.route('/next')
# class total(Resource):
#     @api.expect(model1)
#     def post(self):
#         data = api.payload
#         model1.insert(data)
#         data.pop('_id')
#         return {'kkkk':data}   
        

    

@api.route('/director_movies')
class total(Resource):
    def get(self):
        d = obj.find()
        dm = defaultdict(list)
        for x in d:
            if d:
                dm[x['director']].append(x['name'])
        print(dm)
        d = {}
        l = []
        for s,m in dm.items():
            d[s] = len(m)
        print(d)
        s1,m1 = max(d.items(),key = lambda x:x[1])
        print(s1,m1)

        return {'director': s1,'name': m1 }
@api.route('/higest_rated movies')
class total(Resource):
    def get(self):
        d = obj.find()
        result = []
        for i in d:
            dic ={}
            dic ={'99popularity' : i['99popularity'],'director': i['director'],'genre':i['genre'],'imdb_score':i['imdb_score'],'name':i['name']}
            result.append(dic)
        m = sorted(result,key = lambda x:x['imdb_score'],reverse = True)
        return{'higest_rated_movies':m[:10]}

@api.route('/least_rated movies')
class total(Resource):
    def get(self):
        d = obj.find()
        result = []
        for i in d:
            dic ={}
            dic ={'99popularity' : i['99popularity'],'director': i['director'],'genre':i['genre'],'imdb_score':i['imdb_score'],'name':i['name']}
            result.append(dic)
        m = sorted(result,key = lambda x:x['imdb_score'],reverse = False)
        return{'the least watched movie based on their imdb score':m[:5]}

@api.route('/best_director_of_first_100_movies')
class total(Resource):
    # @cors.crossdomain(origin='*')
    def get(self):
        d = obj.find().limit(100)
        results = []
        l = []
        for i in d:
            dic ={}
            dic ={'99popularity' : i['99popularity'],'director': i['director'],'genre':i['genre'],'imdb_score':i['imdb_score'],'name':i['name']}
            results.append(dic)
        m = max(results,key = lambda x :x['imdb_score'])
        l.append(m)
        print(l)
        return jsonify(l)

@api.route('/popular_genere')
class genere(Resource):
    def get(self):
        d = obj.find()
        gp = defaultdict(int)
        for i in d:
            for j in i['genre']:
                gp[j.strip('')] += i['99popularity']

        m = max(gp.items(),key = lambda x:x[1])

        return {'the popular genere watched by most of the audiance': m}

# @api.route('/search')
# class data(Resource):
#     def get(self):
#         d = obj.find({'director':'rajamouli')
        

# @api.route('/next')
# class movies(Resource):
#     @api.expect(model1)
#     def post(self):
#         data = api.payload
#         model1.insert(data)
#         data.pop('_id')
#         return {'post':data}    
        


if __name__ == '__main__':
    app.run(debug = True,port=5000)