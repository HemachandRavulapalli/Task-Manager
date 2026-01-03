import { StatusBar } from 'expo-status-bar';
import React, { useState } from 'react';
import { 
  KeyboardAvoidingView, 
  StyleSheet, 
  Text, 
  View, 
  TextInput, 
  TouchableOpacity, 
  Keyboard, 
  Platform, 
  FlatList, 
  SafeAreaView 
} from 'react-native';

export default function App() {
  const [task, setTask] = useState('');
  const [taskItems, setTaskItems] = useState([]);

  const handleAddTask = () => {
    if (task.trim()) {
      const newTask = { 
        key: Date.now().toString(), 
        text: task.trim(), 
        completed: false 
      };
      setTaskItems([...taskItems, newTask]);
      setTask('');
      Keyboard.dismiss();
    }
  };

  const toggleComplete = (key) => {
    setTaskItems(taskItems.map(item => 
      item.key === key ? { ...item, completed: !item.completed } : item
    ));
  };

  const renderItem = ({ item }) => {
    return (
      <TouchableOpacity 
        onPress={() => toggleComplete(item.key)} 
        style={styles.item}
        activeOpacity={0.7}
      >
        <View style={styles.itemLeft}>
          <View style={[styles.square, item.completed && styles.squareCompleted]}>
             {item.completed && <Text style={styles.checkmark}>✓</Text>}
          </View>
          <Text style={[styles.itemText, item.completed && styles.itemTextCompleted]}>
            {item.text}
          </Text>
        </View>
        <View style={[styles.circular, item.completed && styles.circularCompleted]} />
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.tasksWrapper}>
        <Text style={styles.sectionTitle}>Task Manager</Text>
        
        <FlatList
          data={taskItems}
          renderItem={renderItem}
          keyExtractor={item => item.key}
          contentContainerStyle={styles.items}
          showsVerticalScrollIndicator={false}
          ListEmptyComponent={
            <Text style={styles.emptyText}>No tasks yet. Add one below!</Text>
          }
        />
      </View>

      <KeyboardAvoidingView 
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.writeTaskWrapper}
      >
        <TextInput 
          style={styles.input} 
          placeholder={'Write a task'} 
          value={task} 
          onChangeText={text => setTask(text)} 
        />
        <TouchableOpacity onPress={handleAddTask}>
          <View style={styles.addWrapper}>
            <Text style={styles.addText}>+</Text>
          </View>
        </TouchableOpacity>
      </KeyboardAvoidingView>
      <StatusBar style="auto" />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E8EAED',
  },
  tasksWrapper: {
    flex: 1,
    paddingTop: 60,
    paddingHorizontal: 20,
  },
  sectionTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 30,
    color: '#1A1A1A',
  },
  items: {
    paddingBottom: 100,
  },
  emptyText: {
    textAlign: 'center',
    color: '#A0A0A0',
    marginTop: 40,
    fontSize: 16,
  },
  writeTaskWrapper: {
    position: 'absolute',
    bottom: 20,
    width: '100%',
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  input: {
    paddingVertical: 15,
    paddingHorizontal: 20,
    backgroundColor: '#FFF',
    borderRadius: 60,
    borderColor: '#C0C0C0',
    borderWidth: 1,
    width: '75%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  addWrapper: {
    width: 60,
    height: 60,
    backgroundColor: '#FFF',
    borderRadius: 60,
    justifyContent: 'center',
    alignItems: 'center',
    borderColor: '#C0C0C0',
    borderWidth: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  addText: {
    fontSize: 24,
    color: '#555',
  },
  item: {
    backgroundColor: '#FFF',
    padding: 15,
    borderRadius: 15,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
    // Soft shadow
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 2,
  },
  itemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flexWrap: 'wrap',
    flex: 1,
  },
  square: {
    width: 24,
    height: 24,
    backgroundColor: '#55BCF6',
    opacity: 0.4,
    borderRadius: 5,
    marginRight: 15,
    alignItems: 'center',
    justifyContent: 'center',
  },
  squareCompleted: {
    backgroundColor: '#55BCF6',
    opacity: 1,
  },
  checkmark: {
    color: 'white', 
    fontSize: 14, 
    fontWeight: 'bold' 
  },
  itemText: {
    maxWidth: '80%',
    fontSize: 16,
    color: '#333',
  },
  itemTextCompleted: {
    textDecorationLine: 'line-through',
    color: '#CCC',
  },
  circular: {
    width: 12,
    height: 12,
    borderColor: '#55BCF6',
    borderWidth: 2,
    borderRadius: 5,
    marginLeft: 10,
  },
  circularCompleted: {
    backgroundColor: '#55BCF6',
  },
});
