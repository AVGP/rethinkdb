// Copyright 2010-2012 RethinkDB, all rights reserved.
#ifndef CLUSTERING_ADMINISTRATION_HTTP_COMBINING_APP_HPP_
#define CLUSTERING_ADMINISTRATION_HTTP_COMBINING_APP_HPP_

#include <map>
#include <string>

#include "http/http.hpp"

/* This class returns results from multiple http_json_app_t's
   get_root methods as a single JSON object */
class combining_http_app_t : public http_app_t {
public:
    explicit combining_http_app_t(std::map<std::string, http_json_app_t *> _components);
    http_res_t handle(const http_req_t &);

private:
    std::map<std::string, http_json_app_t *> components;
};

#endif /* CLUSTERING_ADMINISTRATION_HTTP_COMBINING_APP_HPP_ */
