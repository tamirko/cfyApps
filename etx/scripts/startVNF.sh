#! /bin/bash

myStr1="$(ctx node properties myStr1)"
myStr2="$(ctx node properties myStr2)"
ctx logger info "myStr1 ${myStr1} ..."
ctx logger info "myStr2 ${myStr2} ..."

