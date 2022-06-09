/*package com.example.datatransmission

import retrofit2.Retrofit
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiInterface {
    @GET("photos")
    fun getTest(): String

    @POST
    fun saveUser(@Body UserRequest userRequest)Call<userResponse>

    companion object{
        var BASE_URL = "http://shijie.pythonanywhere.com/"

        fun create() : ApiInterface {

            val retrofit = Retrofit.Builder()
                .addConverterFactory(GsonConverterFactory.create())
                .baseUrl(BASE_URL)
                .build()
            return  retrofit.create((ApiInterface::class.java))
        }
    }
}*/