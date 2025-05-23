package com.azamat.health_monitor_mobile.data.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import com.azamat.health_monitor_mobile.data.entity.ResultEntity

@Dao
interface ResultDao {
    @Insert
    suspend fun insert(result: ResultEntity)

    @Query("DELETE FROM results WHERE taskId = :taskId")
    suspend fun deleteResultsByTaskId(taskId: Int)
}