import android.util.Log
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.wear.compose.material.Card
import androidx.wear.compose.material.Text
import com.azamat.health_monitor_mobile.data.entity.TaskEntity
import com.azamat.health_monitor_mobile.domain.model.TaskDomain

@Composable
fun TaskItem(task: TaskDomain) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
                onClick = { Log.d("Обработано нажатие", "Обработано нажатие")}
    ) {
        Row(modifier = Modifier.padding(12.dp)) {
            Text(
                text = task.scheduledTime.toLocalTime().toString(),
                modifier = Modifier.weight(1f),
                fontWeight = FontWeight.Bold
            )
            Text(text = task.title)
        }
    }
}