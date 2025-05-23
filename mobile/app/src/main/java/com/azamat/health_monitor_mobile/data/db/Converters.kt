package com.azamat.health_monitor_mobile.data.db

import androidx.room.ProvidedTypeConverter
import androidx.room.TypeConverter
import com.azamat.health_monitor_mobile.domain.model.TaskStatus
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

class Converters {

    private val formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME

    @TypeConverter
    fun fromStringList(list: List<String>): String = list.joinToString ( ";" )

    @TypeConverter
    fun toStringList(data: String): List<String> = data.split (";")
    
    @TypeConverter
    fun fromLocalDateTime(value: LocalDateTime?): String? {
        return value?.format(formatter)
    }
    
    @TypeConverter
    fun toLocalDateTime(value: String?): LocalDateTime? {
        return value?.let { LocalDateTime.parse(it, formatter) }
    }
    
    @TypeConverter
    fun fromTaskStatus(status: TaskStatus): String {
        return status.name
    }
    
    @TypeConverter
    fun toTaskStatus(value: String): TaskStatus {
        return TaskStatus.valueOf(value)
    }
}