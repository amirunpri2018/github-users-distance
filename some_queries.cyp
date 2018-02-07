// The top 10 users with the most numerous followinga
match (u:User) with u, size ((u) - [:FOLLOW] -> ())
as following order by following desc limit 10 return u.userId, following

// The top 10 users with the most numerous followersa
match (u:User) with u, size (() - [:FOLLOW] -> (u))
as followers order by followers desc limit 10 return u.userId, followers

// number of users who follow some other users
MATCH (u:User)-[r:FOLLOW]->(:User)
WHERE r IS NOT NULL
RETURN COUNT(u)

// connections of two users
MATCH (src:User { userId: 'threejs-cn' }), (dst:User { userId: 'bww'}),
path = shortestPath((src)-[:FOLLOW*..10]-(dst))
RETURN path

// the top 10 projects with the most numerous members
match (r:Repo)-[:MEMBER] - () return r.repo_name
as project, count(*) as members order by members desc limit 10

// who is contributor on some projects
1) match (u:User)-[m:MEMBER] -> (r:Repo)
where r.repo_name = "tamarakatic/sentiment-analysis-in-amazon-reviews"
return u.userId

// see repos on graph
match (r:Repo)-[:MEMBER] - ()
where r.repo_name = "tamarakatic/sentiment-analysis-in-amazon-reviews"
return r

2) match (u:User)-[m:MEMBER] -> (r:Repo)
where r.repo_name = "novicasarenac/tweets-sentiment"
return u.userId

3) match (u:User)-[m:MEMBER] -> (r:Repo)
where r.repo_name = "VrsajkovIvan33/ISA-2016"
return u.userId

4) match (u:User)-[m:MEMBER] -> (r:Repo)
where r.repo_name = "SrdjanPaunovic/Hackathon2017"
return u.userId
