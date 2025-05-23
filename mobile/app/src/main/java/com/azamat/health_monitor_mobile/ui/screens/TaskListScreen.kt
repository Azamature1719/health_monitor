package com.azamat.health_monitor_mobile.ui.screens

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.compose.foundation.layout.*
import androidx.compose.ui.unit.dp
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.wear.compose.foundation.lazy.ScalingLazyColumn
import androidx.wear.compose.foundation.lazy.items
import androidx.wear.compose.foundation.lazy.rememberScalingLazyListState
import androidx.wear.compose.material.*
import androidx.wear.compose.material.Scaffold
import androidx.wear.compose.material.TimeText
import androidx.wear.compose.material.Vignette
import androidx.wear.compose.material.VignettePosition
import androidx.wear.compose.foundation.lazy.ScalingLazyListState
import com.azamat.health_monitor_mobile.R
import com.azamat.health_monitor_mobile.domain.model.TaskDomain
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import com.azamat.health_monitor_mobile.domain.model.TaskStatus
import com.azamat.health_monitor_mobile.domain.model.TaskType

@Composable
fun TaskListScreen(
    openTasks: List<TaskDomain>,
    doneTasks: List<TaskDomain>,
    onTaskClick: (TaskDomain) -> Unit
) {
    Log.d("TaskListScreen", "TaskListScreen отображён")
    val listState: ScalingLazyListState = rememberScalingLazyListState()

    Scaffold(
        timeText = { TimeText() },
        vignette = {
            Vignette(vignettePosition = VignettePosition.TopAndBottom)
        },
        positionIndicator = {
            PositionIndicator(scalingLazyListState = listState)
        }
    ) {
        val today = LocalDate.now().format(DateTimeFormatter.ofPattern("dd MMMM yyyy"))

        ScalingLazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(top = 30.dp),
            autoCentering = null,
            state = listState
        ) {
            item{
                Text(
                    text = today,
                    color = Color.White,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Medium,
                    textAlign = TextAlign.Center
                )
            }

            if(openTasks.isEmpty() && doneTasks.isEmpty()){
                item{
                    Text(
                        text = "Нет заданий\nна сегодня!",
                        fontSize = 18.sp,
                        color = MaterialTheme.colors.primary,
                        fontWeight = FontWeight.Medium,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(top = 10.dp),
                    )
                }
            }

            if(openTasks.isNotEmpty()){
                item {
                    Text(
                        text = "Открытые задания:",
                        fontWeight = FontWeight.Bold,
                        color = Color.White,
                        fontSize = 18.sp,
                        modifier = Modifier.padding(vertical = 8.dp)
                    )
                }

                items(openTasks) { task ->
                    TaskChip(task = task, onClick = { onTaskClick(task) })
                }
            }
            else if(doneTasks.isNotEmpty()){
                item{
                    Text(
                        text = "Нет новых заданий",
                        fontWeight = FontWeight.Bold,
                        color = Color.White,
                        fontSize = 18.sp,
                        modifier = Modifier.padding(vertical = 8.dp)
                    )
                }
            }


            if(doneTasks.isNotEmpty()){
                item {
                    Text(
                        text = "Выполненные задания:",
                        fontWeight = FontWeight.Bold,
                        color = Color.White,
                        fontSize = 18.sp,
                        modifier = Modifier.padding(vertical = 8.dp)
                    )
                }

                items(doneTasks) { task ->
                    TaskChip(task = task, onClick = { onTaskClick(task) })
                }
            }
        }
    }
}

@Composable
fun TaskChip(task: TaskDomain, onClick: () -> Unit) {

    val backgroundColor = when (task.status) {
        TaskStatus.done -> Color(0xFF79747E)
        TaskStatus.pending-> Color(0xFF342F31)
        TaskStatus.missed -> Color(0xFFF9DEDC)
    }

    val titleColor = when (task.status) {
        TaskStatus.done -> Color(0xFF4A4458)
        TaskStatus.pending-> Color(0xFFFFFFFF)
        TaskStatus.missed -> Color(0xFFB3261E)
    }

    val subtitleColor = when (task.status) {
        TaskStatus.done -> Color(0xFF49454F)
        TaskStatus.pending-> Color(0xFFCCCCCC)
        TaskStatus.missed -> Color(0xFF852221)
    }

    val iconId = when(task.type){
        TaskType.mood -> R.drawable.mood
        TaskType.pressure -> R.drawable.pressure
        TaskType.temperature -> R.drawable.temperature
        TaskType.heart_rate -> R.drawable.heart_rate
        TaskType.saturation -> R.drawable.saturation
        TaskType.other -> R.drawable.heart
    }

    Chip(
        onClick = onClick,
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        label = {
            Text(
                text = "${task.scheduledTime.toLocalTime()} ${task.title}",
                fontWeight = FontWeight.SemiBold,
                color = titleColor,
                fontSize = 18.sp
            )
        },
        secondaryLabel = {
            Text(
                text = task.doctorInfo,
                fontSize = 16.sp,
                color = subtitleColor
            )
        },
        icon = {
            Icon(
                painter = painterResource(id = iconId),
                contentDescription = "heart_icon",
                modifier = Modifier.size(30.dp),
                tint = titleColor
            )
        },
        colors = ChipDefaults.chipColors(
            backgroundColor = backgroundColor
        )
    )
}