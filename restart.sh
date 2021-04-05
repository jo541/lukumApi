#!/bin/bash
app="lukum"
docker stop ${app}
docker start ${app}
