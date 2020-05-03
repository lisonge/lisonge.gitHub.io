/*
 * @Date: 2020-05-03 21:29:57
 * @LastEditors: code
 * @Author: code
 * @LastEditTime: 2020-05-03 21:35:49
 */
console.log('hello fuck')

async function x1(){
    const resp = await fetch('./tests/test1.js')
    console.log(resp)
}
x1()
