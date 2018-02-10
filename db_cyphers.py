from neo4j.v1 import GraphDatabase


class GitHubNeo4jFunctions(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def users_with_numerous_following(self):
        following = {}
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                for record in tx.run("MATCH (u:User) with u, "
                                     "size ((u)-[:FOLLOW]->()) as following order by "
                                     "following desc limit 10 "
                                     "return u.userId, following"):
                    following[record["u.userId"]] = record["following"]

        return following

    def users_with_numerous_followers(self):
        followers = {}
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                for record in tx.run("MATCH (u:User) with u, "
                                     "size (()-[:FOLLOW]->(u)) as followers order by "
                                     "followers desc limit 10 "
                                     "return u.userId, followers"):
                    followers[record["u.userId"]] = record["followers"]

        return followers

    def projects_with_numerous_members(self):
        members = {}
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                for record in tx.run("MATCH (r:Repo)-[:MEMBER] - () "
                                     "return r.repo_name "
                                     "as project, count(*) as members "
                                     "order by members desc limit 10"):
                    members[record["project"]] = record["members"]

        return members

    def users_distance(self, first_user, second_user):
        all_nodes = []
        all_rel = []
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                for record in tx.run("MATCH (src:User { userId: {first} }), "
                                     "(dst:User { userId: {second} }), "
                                     "p = shortestPath((src)-[:FOLLOW*..10]->(dst)) "
                                     "RETURN p", first=first_user, second=second_user):
                    relationships = record["p"].relationships
                    nodes = record["p"].nodes

                    all_nodes = [{
                        "id": node.id,
                        "title": node["userId"],
                        "label": "user"
                    } for node in nodes]

                    def find_node_index(node_id):
                        for index, node in enumerate(all_nodes):
                            if node["id"] == node_id:
                                return index

                    for relationship in relationships:
                        source_id = relationship.start
                        target_id = relationship.end

                        source_idx = find_node_index(source_id)
                        target_idx = find_node_index(target_id)
                        all_rel.append({"source": source_idx, "target": target_idx})

        return {"nodes": all_nodes, "links": all_rel}
