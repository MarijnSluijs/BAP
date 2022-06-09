package com.example.getSmart

import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.*


interface APIService {
    @POST("/json/post")
    suspend fun sendData(@Body Data: List<Data>): Response<ResponseBody>

}